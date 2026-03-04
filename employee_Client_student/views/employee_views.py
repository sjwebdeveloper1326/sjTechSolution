import uuid

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.contrib.auth.models import User

from employee_Client_student.models.employee_model import Employee

# from employee_Client_student.models import Employee

# List all employees
def employee_list(request):
    employees = Employee.objects.all().order_by('-date_of_joining')
    return render(request, 'employeeCRUD/employee_list.html', {'employees': employees})

# Add new employee
def employee_add(request):
    if request.method == "POST":
        try:
            name = request.POST.get('name', '').strip()
            email = request.POST.get('email', '').strip()
            phone = request.POST.get('phone', '').strip()
            role = request.POST.get('role', 'employee')

            # ★★★ Duplicate email check ★★★
            if Employee.objects.filter(email=email).exists():
                messages.error(request, f"Email '{email}' already exists! Ek hi email naal ek hi employee ban sakda hai.")
                return render(request, 'employeeCRUD/employee_form.html')

            if User.objects.filter(email=email).exists():
                messages.error(request, f"Email '{email}' already registered with another account!")
                return render(request, 'employeeCRUD/employee_form.html')

            # Agar email free hai → aage vadh
            emp = Employee(
                name=name,
                phone=phone,
                email=email,
                designation=request.POST.get('designation', ''),
                salary=request.POST.get('salary') or None,
                status=request.POST.get('status', 'active'),
                gender=request.POST.get('gender', ''),
                dob=request.POST.get('dob') or None,
                aadhaar=request.POST.get('aadhaar', ''),
                address=request.POST.get('address', ''),
                date_of_joining=request.POST.get('date_of_joining') or None,
                state=request.POST.get('state', ''),
                city=request.POST.get('city', ''),
                role=role
            )

            if 'photo' in request.FILES:
                emp.photo = request.FILES['photo']

            emp.save()   # ← is vich user create hunda hai te email send hunda (tera save method ton)

            messages.success(request, f"Employee {emp.name} ({emp.emp_id}) successfully add ho gya!")
            return redirect('employee_list')

        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            # optional: print(e)  # development vich dekh lai

    # GET request ya error case
    return render(request, 'employeeCRUD/employee_form.html')


def employee_edit(request, emp_uuid):
    emp = get_object_or_404(Employee, emp_uuid=emp_uuid)

    if request.method == "POST":
        try:
            # Update fields
            emp.name = request.POST['name']
            emp.phone = request.POST['phone']
            emp.email = request.POST['email']
            emp.designation = request.POST.get('designation', '')
            emp.salary = request.POST.get('salary') or None
            emp.status = request.POST.get('status', 'active')
            emp.gender = request.POST.get('gender', '')
            emp.dob = request.POST.get('dob') or None
            emp.aadhaar = request.POST.get('aadhaar', '')
            emp.address = request.POST.get('address', '')
            emp.state = request.POST.get('state', '')
            emp.city = request.POST.get('city', '')
            emp.date_of_joining = request.POST.get('date_of_joining') or None

            # Photo update optional
            if 'photo' in request.FILES:
                emp.photo = request.FILES['photo']

            emp.save()
            messages.success(request, f"Employee {emp.name} updated successfully!")

            # ✅ Redirect properly using URL parameter name 'emp_uuid'
            if request.user.is_authenticated:
                if hasattr(request.user, 'employee') and request.user.employee.emp_uuid == emp.emp_uuid:
                    return redirect('dashboard_employee', emp_uuid=emp.emp_uuid)

            # Admin / HR redirect
            return redirect('employee_list')

        except Exception as e:
            messages.error(request, f"Error: {e}")

    return render(request, 'employeeCRUD/employee_form.html', {'emp': emp})

# Delete employee
def employee_delete(request, emp_uuid):
    emp = get_object_or_404(Employee, emp_uuid=emp_uuid)
    if request.method == "POST":
        emp.delete()
        messages.success(request, f"Employee {emp.name} deleted!")
        return redirect('employee_list')
    return render(request, 'employeeCRUD/employee_delete.html', {'emp': emp})