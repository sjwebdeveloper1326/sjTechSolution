from decimal import Decimal
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone

from employee_Client_student.models.student_model import Student
from employee_Client_student.models.employee_model import Employee
from mainApp.models import Course   # assuming this exists
# from employee_Client_student.models.course_model import Course       # assuming this exists


def student_list(request):
    students = Student.objects.all().order_by('-date_of_joining')
    return render(request, 'studentCRUD/student_list.html', {
        'students': students
    })


def student_add(request):
    if request.method == "POST":
        try:
            fee_paid_str = request.POST.get('feePaid', '').strip()
            fee_paid_value = None if not fee_paid_str else Decimal(fee_paid_str)
            student = Student(
                name=request.POST.get('name', '').strip(),
                phone=request.POST.get('phone', '').strip(),
                email=request.POST.get('email', '').strip(),
                feePaid=fee_paid_value,
                status=request.POST.get('status', 'active'),
                gender=request.POST.get('gender', 'male'),
                dob=request.POST.get('dob'),
                aadhaar=request.POST.get('aadhaar', '').strip(),
                address=request.POST.get('address', '').strip(),
                date_of_joining=request.POST.get('date_of_joining') or timezone.now().date(),
            )

            # Handle multi-select courses
            course_ids = request.POST.getlist('course_ids')
            if course_ids:
                student.course_ids = [int(cid) for cid in course_ids if cid.isdigit()]

            # Handle single select jointBy (emp_uuid)
            joint_by_uuid = request.POST.get('joint_by_uuid')
            if joint_by_uuid:
                student.jointBy = joint_by_uuid

            # Handle photo
            if 'photo' in request.FILES:
                student.photo = request.FILES['photo']

            student.save()  # this will auto-generate student_id

            messages.success(request, f"Student {student.name} ({student.student_id}) enrolled successfully!")
            return redirect('student_list')

        except Exception as e:
            messages.error(request, f"Error saving student: {str(e)}")

    # GET request - prepare context
    context = {
        'action': 'Add',
        'courses': Course.objects.all().order_by('order', 'title'),
        'employees': Employee.objects.filter(status='active').order_by('name'),
        'all_students': Student.objects.all().order_by('name'),  # if you need for jointStudents
    }
    return render(request, 'studentCRUD/student_form.html', context)


def student_edit(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        try:
            fee_paid_str = request.POST.get('feePaid', '').strip()
            fee_paid_value = None if not fee_paid_str else Decimal(fee_paid_str)
            student.name = request.POST.get('name', '').strip()
            student.phone = request.POST.get('phone', '').strip()
            student.email = request.POST.get('email', '').strip()
            student.feePaid = fee_paid_value
            student.status = request.POST.get('status', 'active')
            student.gender = request.POST.get('gender', 'male')
            student.dob = request.POST.get('dob')
            student.aadhaar = request.POST.get('aadhaar', '').strip()
            student.address = request.POST.get('address', '').strip()
            student.date_of_joining = request.POST.get('date_of_joining') or timezone.now().date()

            # Courses multi-select
            course_ids = request.POST.getlist('course_ids')
            student.course_ids = [int(cid) for cid in course_ids if cid.isdigit()] if course_ids else None

            # jointBy single select
            joint_by_uuid = request.POST.get('joint_by_uuid')
            student.jointBy = joint_by_uuid if joint_by_uuid else None

            # Photo update (replace if new one uploaded)
            if 'photo' in request.FILES:
                student.photo = request.FILES['photo']

            student.save()

            messages.success(request, f"Student {student.name} ({student.student_id}) updated successfully!")
            return redirect('student_list')

        except Exception as e:
            messages.error(request, f"Error updating student: {str(e)}")

    # GET request
    context = {
        'action': 'Edit',
        'student': student,
        'courses': Course.objects.all().order_by('order', 'title'),
        'employees': Employee.objects.filter(status='active').order_by('name'),
        'all_students': Student.objects.exclude(id=id).order_by('name'),
    }
    return render(request, 'studentCRUD/student_form.html', context)


def student_delete(request, id):
    student = get_object_or_404(Student, id=id)
    
    if request.method == "POST":
        student_name = student.name
        student.delete()
        messages.success(request, f"Student {student_name} deleted successfully!")
        return redirect('student_list')

    return render(request, 'studentCRUD/student_delete.html', {'student': student})