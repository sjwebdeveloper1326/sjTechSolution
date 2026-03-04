
from django.shortcuts import render, redirect, get_object_or_404

from employee_Client_student.models.student_model import Student

def student_dashboard(request,student_id):
    student = get_object_or_404(Student, student_id=student_id)

    # timesheet connected to employee
    timesheet = Student.timesheet_set.all().order_by('-date') if hasattr(student, 'timesheet_set') else []

    return render(request,  "studentCRUD/dashboard_student.html", {
        "student": student,
        "timesheet": timesheet,
        "profile_id": student.student_id,
        "user_type": "student",
    })
    # return render(request, "studentCRUD/dashboard_student.html")