from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from employee_Client_student.models import Employee


ADMIN_LEVEL_ROLES = {"admin", "manager", "account-manager"}


def get_logged_employee(user):
    if not user.is_authenticated:
        return None

    if hasattr(user, "employee"):
        return user.employee

    emp_id = user.username.split("@")[-1]
    return Employee.objects.filter(emp_id=emp_id).first()


def is_admin_level_user(user):
    if user.is_superuser:
        return True

    employee = get_logged_employee(user)
    return bool(employee and employee.role in ADMIN_LEVEL_ROLES)


def admin_level_required(view_func):
    @login_required(login_url="login")
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if is_admin_level_user(request.user):
            return view_func(request, *args, **kwargs)

        messages.error(request, "Permission denied.")
        return redirect("home")

    return _wrapped_view
