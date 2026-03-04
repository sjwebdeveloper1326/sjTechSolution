

import uuid

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views

from employee_Client_student.models.employee_model import Employee
from employee_Client_student.models.student_model import Student

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Invalid Username or Password")
            return render(request, "auth/login.html")

        # STUDENT LOGIN
        if "SJS" in username:
            try:
                student_id = username.split("@")[-1]
                stu = Student.objects.get(student_id=student_id)
            except Student.DoesNotExist:
                messages.error(request, "Student record not found!")
                return render(request, "auth/login.html")

            login(request, user)
            return redirect("dashboard_student", student_id=stu.student_id)

        # EMPLOYEE / TEACHER / CLIENT LOGIN
        try:
            emp_id = username.split("@")[-1]
            emp = Employee.objects.get(emp_id=emp_id)
        except Employee.DoesNotExist:
            messages.error(request, "Employee record not found!")
            return render(request, "auth/login.html")

        login(request, user)

        # 🔐 ROLE BASED REDIRECT
        if emp.role in ["employee", "teacher"]:
            return redirect("dashboard_employee", emp_uuid=emp.emp_uuid)

        elif emp.role == "client":
            return redirect("dashboard_client", emp_id=emp.emp_id)

        else:
            messages.error(request, "Unauthorized role")
            return redirect("login")

    return render(request, "auth/login.html")


def logout_view(request):
    logout(request)
    return redirect('home')