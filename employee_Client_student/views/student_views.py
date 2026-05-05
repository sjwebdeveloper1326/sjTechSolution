from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone

from employee_Client_student.models.student_model import Student
from employee_Client_student.models.employee_model import Employee
from mainApp.models import Course
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def student_list(request):
    students = Student.objects.all().order_by('-date_of_joining')
    return render(request, 'studentCRUD/student_list.html', {
        'students': students
    })

 # adjust import path as needed
@login_required(login_url='login')
def student_add(request):
    if request.method == "POST":
        try:
            name = request.POST.get('name', '').strip()
            email = request.POST.get('email', '').strip()
            phone = request.POST.get('phone', '').strip()

            # ─── Email uniqueness checks ─────────────────────────────────────
            if not email:
                messages.error(request, "Email field is required!")
                return render(request, 'studentCRUD/student_form.html', get_context())

            if Student.objects.filter(email=email).exists():
                messages.error(request, f"Email '{email}' already exists ! Please use another email.")
                return render(request, 'studentCRUD/student_form.html', get_context())

            if Employee.objects.filter(email=email).exists():
                # messages.error(request, f"Email '{email}' is already used by an employee! Please use a different email.")
                messages.error(request, f"Email '{email}'  already exists ! Please use another email.")
                return render(request, 'studentCRUD/student_form.html', get_context())

            if User.objects.filter(email=email).exists():
                # messages.error(request, f"Email '{email}' is already registered in the system (user account)! Please choose another.")
                messages.error(request, f"Email '{email}' already exists ! Please use another email.")
                return render(request, 'studentCRUD/student_form.html', get_context())
            # ────────────────────────────────────────────────────────────────

            fee_paid_str = request.POST.get('feePaid', '').strip()
            fee_paid_value = None if not fee_paid_str else Decimal(fee_paid_str)

            dob_raw = request.POST.get('dob', '').strip()
            dob = dob_raw if dob_raw else None

            joining_raw = request.POST.get('date_of_joining', '').strip()
            date_of_joining = joining_raw if joining_raw else timezone.now().date()

            student = Student(
                name=name,
                phone=phone,
                email=email,
                feePaid=fee_paid_value,
                status=request.POST.get('status', 'active'),
                gender=request.POST.get('gender', 'male'),
                dob=dob,
                aadhaar=request.POST.get('aadhaar', '').strip(),
                address=request.POST.get('address', '').strip(),
                date_of_joining=date_of_joining,
                role='student'
            )

            # Courses - safe conversion
            course_ids_raw = request.POST.getlist('course_ids')
            valid_course_ids = []
            for cid in course_ids_raw:
                stripped = cid.strip()
                if stripped.isdigit():
                    valid_course_ids.append(int(stripped))
            student.course_ids = valid_course_ids if valid_course_ids else None

            joint_by_uuid = (
                request.POST.get('referred_student_uuid', '').strip()
                or request.POST.get('joint_by_uuid', '').strip()
            )
            student.jointBy = joint_by_uuid if joint_by_uuid else None

            if 'photo' in request.FILES:
                student.photo = request.FILES['photo']

            student.save()

            messages.success(request, f"Student {student.name} ({student.student_id}) enrolled successfully!")
            return redirect('student_list')

        except Exception as e:
            messages.error(request, f"Error saving student: {str(e)}")

    # GET or error case
    return render(request, 'studentCRUD/student_form.html', get_context())


def get_context():
    """Helper to avoid code duplication"""
    return {
        'action': 'Add',
        'courses': Course.objects.all().order_by('order', 'title'),
        'employees': Employee.objects.filter(status='active').order_by('name'),
        'all_students': Student.objects.all().order_by('name'),
    }

# def student_edit(request, stu_uuid):
#     student = get_object_or_404(Student, stu_uuid=stu_uuid)

#     if request.method == "POST":
#         try:
#             fee_paid_str = request.POST.get('feePaid', '').strip()
#             fee_paid_value = None if not fee_paid_str else Decimal(fee_paid_str)

#             dob_raw = request.POST.get('dob', '').strip()
#             student.dob = dob_raw if dob_raw else None

#             joining_raw = request.POST.get('date_of_joining', '').strip()
#             student.date_of_joining = joining_raw if joining_raw else timezone.now().date()

#             student.name = request.POST.get('name', '').strip()
#             student.phone = request.POST.get('phone', '').strip()
#             student.email = request.POST.get('email', '').strip()
#             student.feePaid = fee_paid_value
#             student.status = request.POST.get('status', 'active')
#             student.gender = request.POST.get('gender', 'male')
#             student.aadhaar = request.POST.get('aadhaar', '').strip()
#             student.address = request.POST.get('address', '').strip()

#             # Courses - safe conversion
#             course_ids_raw = request.POST.getlist('course_ids')
#             valid_course_ids = []
#             for cid in course_ids_raw:
#                 stripped = cid.strip()
#                 if stripped.isdigit():
#                     valid_course_ids.append(int(stripped))
#             student.course_ids = valid_course_ids if valid_course_ids else None

#             joint_by_uuid = request.POST.get('joint_by_uuid', '').strip()
#             student.jointBy = joint_by_uuid if joint_by_uuid else None

#             if 'photo' in request.FILES:
#                 student.photo = request.FILES['photo']

#             student.save()

#             messages.success(request, f"Profile updated successfully!")
#             # Redirect to student dashboard instead of student_list
#             return redirect('dashboard_student', stu_uuid=student.stu_uuid)

#         except Exception as e:
#             messages.error(request, f"Error updating profile: {str(e)}")

#     context = {
#         'action': 'Edit',
#         'student': student,
#         'courses': Course.objects.all().order_by('order', 'title'),
#         'employees': Employee.objects.filter(status='active').order_by('name'),
#         'all_students': Student.objects.exclude(stu_uuid=stu_uuid).order_by('name'),
#     }
#     return render(request, 'studentCRUD/student_form.html', context)
@login_required(login_url='login')
def student_edit(request, stu_uuid):
    student = get_object_or_404(Student, stu_uuid=stu_uuid)

    if request.method == "POST":
        try:
            fee_paid_str = request.POST.get('feePaid', '').strip()
            fee_paid_value = None if not fee_paid_str else Decimal(fee_paid_str)

            dob_raw = request.POST.get('dob', '').strip()
            student.dob = dob_raw if dob_raw else None

            joining_raw = request.POST.get('date_of_joining', '').strip()
            student.date_of_joining = joining_raw if joining_raw else timezone.now().date()

            student.name = request.POST.get('name', '').strip()
            student.phone = request.POST.get('phone', '').strip()
            student.email = request.POST.get('email', '').strip()
            student.feePaid = fee_paid_value
            student.status = request.POST.get('status', 'active')
            student.gender = request.POST.get('gender', 'male')
            student.aadhaar = request.POST.get('aadhaar', '').strip()
            student.address = request.POST.get('address', '').strip()

            course_ids_raw = request.POST.getlist('course_ids')
            valid_course_ids = []

            for cid in course_ids_raw:
                stripped = cid.strip()
                if stripped.isdigit():
                    valid_course_ids.append(int(stripped))

            student.course_ids = valid_course_ids if valid_course_ids else None

            joint_by_uuid = (
                request.POST.get('referred_student_uuid', '').strip()
                or request.POST.get('joint_by_uuid', '').strip()
            )
            student.jointBy = joint_by_uuid if joint_by_uuid else None

            if 'photo' in request.FILES:
                student.photo = request.FILES['photo']

            student.save()

            messages.success(request, "Profile updated successfully!")

            user = request.user

            # STUDENT SELF UPDATE
            if user.is_authenticated and "SJS" in user.username:
                try:
                    student_id = user.username.split("@")[-1]
                    logged_student = Student.objects.get(student_id=student_id)

                    if logged_student.stu_uuid == student.stu_uuid:
                        return redirect("dashboard_student", stu_uuid=student.stu_uuid)

                except Student.DoesNotExist:
                    pass

            # ADMIN / MANAGER / EMPLOYEE UPDATE
            return redirect("student_list")

        except Exception as e:
            messages.error(request, f"Error updating profile: {str(e)}")

    context = {
        'action': 'Edit',
        'student': student,
        'courses': Course.objects.all().order_by('order', 'title'),
        'employees': Employee.objects.filter(status='active').order_by('name'),
        'all_students': Student.objects.exclude(stu_uuid=stu_uuid).order_by('name'),
    }

    return render(request, 'studentCRUD/student_form.html', context)


@login_required(login_url='login')
def student_delete(request, stu_uuid):
    try:
        student = get_object_or_404(Student, stu_uuid=stu_uuid)

        if request.method == "POST":
            student_name = student.name
            student.delete()

            messages.success(request, f"Student {student_name} deleted successfully!")
            return redirect('student_list')

        return render(request, 'studentCRUD/student_delete.html', {'student': student})

    except Exception as e:
        messages.error(request, f"Error deleting student: {str(e)}")
        return redirect('student_list')

# def student_delete(request, stu_uuid):
#     student = get_object_or_404(Student, stu_uuid=stu_uuid)
    
#     if request.method == "POST":
#         student_name = student.name
#         student.delete()
#         messages.success(request, f"Student {student_name} deleted successfully!")
#         return redirect('student_list')

#     return render(request, 'studentCRUD/student_delete.html', {'student': student})
