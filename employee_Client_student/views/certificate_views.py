import base64
from io import BytesIO

import qrcode
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles import finders
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from PIL import Image, ImageDraw, ImageFont

from employee_Client_student.models import Employee, Student
from mainApp.models import Course
from utils.site_urls import absolute_url, request_base_url


def _employee_for_user(user):
    return Employee.objects.filter(user=user).first()


def _student_for_user(user):
    return Student.objects.filter(user=user).first()


def _student_courses(student):
    if not student.course_ids:
        return Course.objects.none()

    ids = []
    for course_id in student.course_ids:
        if str(course_id).isdigit():
            ids.append(int(course_id))

    return Course.objects.filter(id__in=ids).order_by('order', 'title')


def _certificate_course(student):
    return _student_courses(student).first()


def _can_manage_certificate(user, student):
    employee = _employee_for_user(user)
    if not employee:
        return False

    role = (employee.role or '').lower()
    if role in ['admin', 'manager', 'account-manager']:
        return True

    if role in ['teacher', 'instructor', 'trainer']:
        employee_uuid = str(employee.emp_uuid)
        for course in _student_courses(student):
            teacher_ids = course.teacher_ids or []
            if isinstance(teacher_ids, list) and employee_uuid in teacher_ids:
                return True

        joint_by = student.jointBy
        if isinstance(joint_by, str) and joint_by == employee_uuid:
            return True
        if isinstance(joint_by, list) and employee_uuid in joint_by:
            return True

    return False


def _can_download_certificate(user, student):
    own_student = _student_for_user(user)
    if own_student and own_student.pk == student.pk:
        return student.certificate_approved

    return _can_manage_certificate(user, student)


def _qr_data_uri(value):
    qr_image = qrcode.make(value)
    buffer = BytesIO()
    qr_image.save(buffer, format='PNG')
    encoded = base64.b64encode(buffer.getvalue()).decode('ascii')
    return f'data:image/png;base64,{encoded}'


def _font(size, bold=False, italic=False):
    names = []
    if bold and italic:
        names = ['arialbi.ttf', 'georgiaz.ttf']
    elif bold:
        names = ['arialbd.ttf', 'georgiab.ttf']
    elif italic:
        names = ['ariali.ttf', 'georgiai.ttf']
    else:
        names = ['arial.ttf', 'georgia.ttf']

    for name in names:
        try:
            return ImageFont.truetype(f'C:/Windows/Fonts/{name}', size)
        except Exception:
            continue
    return ImageFont.load_default()


def _center_text(draw, xy, text, font, fill):
    x, y = xy
    bbox = draw.textbbox((0, 0), text, font=font)
    draw.text((x - (bbox[2] - bbox[0]) / 2, y), text, font=font, fill=fill)


def _pillow_certificate_pdf(context):
    width, height = 1684, 1191
    navy = '#121820'
    gold = '#FF6DBA'
    gold_soft = '#FFD1EA'
    text = '#1F2630'

    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)

    draw.rectangle((20, 20, width - 20, height - 20), outline=gold, width=5)
    draw.polygon([(0, 0), (310, 0), (0, 240)], fill=navy)
    draw.polygon([(width, height), (width - 310, height), (width, height - 240)], fill=navy)
    draw.line((0, 230, 305, 0), fill=gold_soft, width=28)
    draw.line((width - 305, height, width, height - 230), fill=gold_soft, width=28)

    draw.text((width - 380, 64), f"Certificate ID: {context['certificate_id']}", font=_font(18), fill=text)
    draw.text((width - 300, 92), f"Date: {context['approved_date'].strftime('%B %d, %Y')}", font=_font(18), fill=text)

    logo_path = finders.find('assets/images/SJ_T_logo.png')
    if logo_path:
        logo = Image.open(logo_path).convert('RGBA')
        logo.thumbnail((135, 100))
        img.paste(logo, ((width - logo.width) // 2, 45), logo)

    _center_text(draw, (width / 2, 155), 'SJ TECH SOLUTION', _font(36, bold=True), navy)
    _center_text(draw, (width / 2, 202), 'Learn Today, Lead Tomorrow', _font(18), text)
    _center_text(draw, (width / 2, 290), 'CERTIFICATE', _font(86, bold=True), navy)
    _center_text(draw, (width / 2, 390), 'OF COMPLETION', _font(43, bold=True), gold)
    draw.line((550, 470, 780, 470), fill=gold, width=2)
    draw.line((905, 470, 1135, 470), fill=gold, width=2)
    _center_text(draw, (width / 2, 455), '*', _font(34, bold=True), gold)

    _center_text(draw, (width / 2, 525), 'This is to certify that', _font(28), text)
    _center_text(draw, (width / 2, 590), context['student'].name, _font(62, italic=True), navy)
    draw.line((490, 660, 1194, 660), fill=gold, width=2)
    _center_text(draw, (width / 2, 695), 'has successfully completed the', _font(26), text)
    course_title = context['course'].title if context['course'] else 'SJ Tech Solution Course'
    _center_text(draw, (width / 2, 735), course_title, _font(31, bold=True), navy)
    _center_text(draw, (width / 2, 775), 'offered by SJ Tech Solution.', _font(25), text)
    _center_text(draw, (width / 2, 830), "This certificate acknowledges the recipient's dedication, hard work,", _font(23), text)
    _center_text(draw, (width / 2, 860), 'and successful completion of all course requirements.', _font(23), text)

    draw.ellipse((115, 340, 320, 545), fill=navy, outline=gold, width=14)
    draw.ellipse((135, 360, 300, 525), outline=gold_soft, width=4)
    _center_text(draw, (217, 405), 'COURSE', _font(18, bold=True), 'white')
    _center_text(draw, (217, 430), 'COMPLETED', _font(18, bold=True), 'white')

    verify_url = context['verify_url']
    qr = qrcode.make(verify_url).convert('RGB').resize((150, 150))
    draw.rectangle((1345, 520, 1535, 710), outline=gold, width=4)
    img.paste(qr, (1365, 540))
    _center_text(draw, (1440, 735), 'Verify Certificate', _font(17, bold=True), navy)

    details_y = 925
    details = [
        ('COURSE DURATION', context['course'].duration_display if context['course'] else '-'),
        ('COMPLETED ON', context['approved_date'].strftime('%b %d, %Y')),
        ('PERFORMANCE', context['student'].certificate_performance or 'Excellent'),
    ]
    for index, (label, value) in enumerate(details):
        x = 475 + index * 300
        draw.ellipse((x - 55, details_y - 20, x - 5, details_y + 30), fill=navy)
        icon_text = ['B', 'C', 'P'][index]
        _center_text(draw, (x - 30, details_y - 13), icon_text, _font(20, bold=True), 'white')
        draw.text((x + 10, details_y - 18), label, font=_font(15, bold=True), fill=text)
        draw.text((x + 10, details_y + 5), value, font=_font(21, bold=True), fill=navy)

    _center_text(draw, (width / 2, 1020), 'Syed Junaid', _font(32, italic=True), navy)
    draw.line((690, 1070, 995, 1070), fill=gold, width=2)
    _center_text(draw, (width / 2, 1082), 'Syed Junaid', _font(22, bold=True), navy)
    _center_text(draw, (width / 2, 1112), 'Founder & CEO, SJ Tech Solution', _font(18), text)
    draw.rectangle((1375, 990, 1540, 1085), outline=gold, width=3)
    _center_text(draw, (1457, 1020), 'COMPANY', _font(18, bold=True), gold)
    _center_text(draw, (1457, 1046), 'STAMP', _font(18, bold=True), gold)
    draw.text((60, 1130), f"www.{context['company_site']}", font=_font(18, bold=True), fill=navy)

    buffer = BytesIO()
    img.save(buffer, format='PDF', resolution=144.0)
    return buffer.getvalue()


def _certificate_context(request, student):
    course = _certificate_course(student)
    verify_url = absolute_url(
        reverse('certificate_verify', kwargs={'stu_uuid': student.stu_uuid}),
        request,
    )
    approved_date = student.certificate_approved_at or timezone.now()

    return {
        'student': student,
        'course': course,
        'certificate_id': student.certificate_id,
        'approved_date': approved_date,
        'verify_url': verify_url,
        'qr_data_uri': _qr_data_uri(verify_url),
        'company_site': request_base_url(request).replace('https://', '').replace('http://', '').rstrip('/'),
        'signature_image': getattr(settings, 'CERTIFICATE_SIGNATURE_IMAGE', ''),
        'stamp_image': getattr(settings, 'CERTIFICATE_STAMP_IMAGE', '/static/assets/images/stamp_transprent.png'),
    }


@login_required(login_url='login')
def certificate_approve(request, stu_uuid):
    student = get_object_or_404(Student, stu_uuid=stu_uuid)

    if request.method != 'POST':
        return redirect('student_list')

    if not _can_manage_certificate(request.user, student):
        return HttpResponseForbidden('You are not allowed to approve this certificate.')

    student.certificate_approved = True
    student.certificate_approved_by = request.user
    student.certificate_approved_at = timezone.now()
    student.certificate_performance = request.POST.get('performance', 'Excellent').strip() or 'Excellent'
    student.save(update_fields=[
        'certificate_approved',
        'certificate_approved_by',
        'certificate_approved_at',
        'certificate_performance',
    ])

    messages.success(request, f'Certificate approved for {student.name}.')
    next_url = request.POST.get('next') or 'student_list'
    return redirect(next_url)


@login_required(login_url='login')
def certificate_preview(request, stu_uuid):
    student = get_object_or_404(Student, stu_uuid=stu_uuid)
    if not _can_download_certificate(request.user, student):
        return HttpResponseForbidden('Certificate is not available yet.')

    return render(request, 'certificates/student_certificate.html', _certificate_context(request, student))


@login_required(login_url='login')
def certificate_download(request, stu_uuid):
    student = get_object_or_404(Student, stu_uuid=stu_uuid)
    if not _can_download_certificate(request.user, student):
        return HttpResponseForbidden('Certificate is not available yet.')

    context = _certificate_context(request, student)

    try:
        from weasyprint import HTML

        html = render_to_string(
            'certificates/student_certificate.html',
            context,
            request=request,
        )
        pdf = HTML(string=html, base_url=request.build_absolute_uri('/')).write_pdf()
    except (ImportError, OSError):
        pdf = _pillow_certificate_pdf(context)

    response = HttpResponse(pdf, content_type='application/pdf')
    filename = f'{student.student_id}-certificate.pdf'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


def certificate_verify(request, stu_uuid):
    student = get_object_or_404(Student, stu_uuid=stu_uuid, certificate_approved=True)
    return render(request, 'certificates/certificate_verify.html', _certificate_context(request, student))
