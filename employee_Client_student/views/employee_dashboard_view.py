import uuid

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from employee_Client_student.models import Employee, Student

def employee_dashboard(request, emp_uuid):
    employee = get_object_or_404(
        Employee,
        emp_uuid=emp_uuid,
        user=request.user
    )
    timesheets = employee.timesheets.all().order_by('-date')
    context = {
        "employee": employee,
        "timesheets": timesheets,
        "profile_uuid": employee.emp_uuid,
        "profile_id": employee.emp_id,
        "user_type": "employee",
        "emp_uuid": employee.emp_uuid,
    }
    return render(
        request,
        "employeeCRUD/dashboard_employee.html",
        context
    )