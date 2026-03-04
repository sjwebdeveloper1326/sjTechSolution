# def profile_id(request):
#     if request.user.is_authenticated:
#         username = request.user.username
#         if "_" in username:
#             return {"profile_id": username.split("_")[-1]}
#     return {}

# from employee.models import Employee, Student

from employee_Client_student.models import Employee, Student


def profile_id(request):
    context = {
        "profile_id": None,
        "student": None,
        "employee": None,
    }

    if request.user.is_authenticated:
        username = request.user.username

        # STUDENT
        if "SJS" in username:
            try:
                student_id = username.split("@")[-1]
                student = Student.objects.get(student_id=student_id)
                context.update({
                    "profile_id": student.student_id,
                    "student": student,
                })
            except Student.DoesNotExist:
                pass

        # EMPLOYEE
        elif "SJE" in username:
            try:
                emp_id = username.split("@")[-1]
                employee = Employee.objects.get(emp_id=emp_id)
                context.update({
                    "profile_id": employee.emp_id,
                    "employee": employee,
                })
            except Employee.DoesNotExist:
                pass

        # TEACHER
        elif "SJT" in username:
            try:
                emp_id = username.split("@")[-1]
                employee = Employee.objects.get(emp_id=emp_id)
                context.update({
                    "profile_id": employee.emp_id,
                    "employee": employee,
                })
            except Employee.DoesNotExist:
                pass

    return context