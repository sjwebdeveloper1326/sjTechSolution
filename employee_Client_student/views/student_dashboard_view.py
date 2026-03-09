from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from employee_Client_student.models import Student
from employee_Client_student.models.employee_model import Employee

# def student_dashboard(request, stu_uuid):
#     student = get_object_or_404(
#         Student,
#         stu_uuid=stu_uuid,
#         user=request.user  # optional security
#     )

#     # Timesheet - agar student model vich relation hai (related_name='timesheets')
#     timesheets = student.timesheets.all().order_by('-date') if hasattr(student, 'timesheets') else []

#     context = {
#         "student": student,
#         "timesheets": timesheets,
#         "profile_uuid": student.stu_uuid,
#         "profile_id": student.student_id,
#         "user_type": "student",
#         "stu_uuid": student.stu_uuid,  # template vich use layi
#     }
#     return render(
#         request,
#         "studentCRUD/dashboard_student.html",
#         context
#     )
from django.shortcuts import render, get_object_or_404
from mainApp.models import Course
from employee_Client_student.models import Student, Employee

def student_dashboard(request, stu_uuid):
    student = get_object_or_404(
        Student,
        stu_uuid=stu_uuid,
        user=request.user  # security: only own dashboard
    )

    # Timesheets (assuming related_name='timesheets')
    timesheets = student.timesheets.all().order_by('-date') if hasattr(student, 'timesheets') else []

    # Fetch teacher (if jointBy exists)
    teacher = None
    if student.jointBy:
        try:
            teacher = Employee.objects.filter(emp_uuid=student.jointBy).first()
        except Exception:
            pass  # silent fail or log

    # Fetch enrolled courses from course_ids (JSONField)
    enrolled_courses = []
    if student.course_ids:
        try:
            # If course_ids is list of integers (most common)
            course_ids = [int(cid) for cid in student.course_ids if str(cid).isdigit()]
            enrolled_courses = Course.objects.filter(id__in=course_ids).order_by('order', 'title')
        except (ValueError, TypeError):
            # If course_ids contains UUID strings (less common)
            try:
                from uuid import UUID
                course_uuids = [UUID(cid) for cid in student.course_ids if cid]
                enrolled_courses = Course.objects.filter(uuid__in=course_uuids)
            except:
                pass  # invalid IDs → show empty

    context = {
        "student": student,
        "timesheets": timesheets,
        "teacher": teacher,
        "enrolled_courses": enrolled_courses,  # ← THIS WAS MISSING!
        "stu_uuid": student.stu_uuid,
        "profile_uuid": student.stu_uuid,
        "profile_id": student.student_id,
        "user_type": "student",
    }

    return render(request, "studentCRUD/dashboard_student.html", context)