# employee/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import Employee, Student
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Invalid Username or Password")
            return render(request, "auth/login.html")

        # EMPLOYEE LOGIN
        if role == "employee" and "SJE" in username:
            try:
                emp = Employee.objects.get(emp_id=username.split("_")[-1])
            except:
                messages.error(request, "Employee record not found!")
                return render(request, "auth/login.html")

            login(request, user)
            return redirect("dashboard_employee", emp_id=emp.emp_id)

        # STUDENT LOGIN
        elif role == "student" and "SJS" in username:
            try:
                stu = Student.objects.get(student_id=username.split("_")[-1])
            except:
                messages.error(request, "Student not found!")
                return render(request, "auth/login.html")

            login(request, user)
            return redirect("dashboard_student", student_id=stu.student_id)

        else:
            messages.error(request, "Role does not match the account type!")
            return render(request, "auth/login.html")

    return render(request, "auth/login.html")


def logout_view(request):
    logout(request)
    return redirect('home')

# password reset email send hone ke baad SUCCESS MESSAGE ke liye
class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'auth/password_reset.html'
    email_template_name = 'emails/password_reset_email.html'
    html_email_template_name = 'emails/password_reset_email.html'
    subject_template_name = 'emails/password_reset_subject.txt'

    def form_valid(self, form):
        email = form.cleaned_data.get('email')

        # superadmin check
        from django.contrib.auth.models import User
        try:
            user = User.objects.get(email=email)
            if user.is_superuser:
                messages.error(
                    self.request,
                    "You can change password of this mail from hare!."
                )
                return redirect('password_reset')
        except User.DoesNotExist:
            pass

        messages.success(
            self.request,
            "Password reset link aapke email par bhej diya gaya hai."
        )
        return super().form_valid(form)



# passwod change start...

class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    def get(self, request, *args, **kwargs):
        messages.success(request, "Your password has been reset successfully! Please login again.")
        return redirect('login')   # ← yaha apne login URL ka name daalna

# passwod change end...
def register_view(request):
    return render(request, "auth/register.html")

# def dashboard_employee(request):
#     return render(request, "employeeCRUD/dashboard_employee.html")

def dashboard_employee(request, emp_id):
    employee = get_object_or_404(Employee, emp_id=emp_id)

    # timesheet connected to employee
    timesheet = employee.timesheet_set.all().order_by('-date') if hasattr(employee, 'timesheet_set') else []

    return render(request,  "employeeCRUD/dashboard_employee.html", {
        "employee": employee,
        "timesheet": timesheet
    })


def dashboard_student(request,student_id):
    student = get_object_or_404(Student, student_id=student_id)

    # timesheet connected to employee
    timesheet = Student.timesheet_set.all().order_by('-date') if hasattr(student, 'timesheet_set') else []

    return render(request,  "studentCRUD/dashboard_student.html", {
        "student": student,
        "timesheet": timesheet
    })
    # return render(request, "studentCRUD/dashboard_student.html")


# List all employees
def employee_list(request):
    employees = Employee.objects.all().order_by('-date_of_joining')
    return render(request, 'employeeCRUD/employee_list.html', {'employees': employees})

# Add new employee
def employee_add(request):
    if request.method == "POST":
        try:
            emp = Employee(
                name=request.POST['name'],
                phone=request.POST['phone'],
                email=request.POST['email'],
                designation=request.POST['designation'],
                salary=request.POST['salary'],
                status=request.POST['status'],
                gender=request.POST['gender'],
                dob=request.POST['dob'],
                aadhaar=request.POST.get('aadhaar', ''),
                address=request.POST['address'],
                date_of_joining=request.POST['date_of_joining'],
            )
            if 'photo' in request.FILES:
                emp.photo = request.FILES['photo']
            emp.save()
            messages.success(request, f"Employee {emp.name} ({emp.emp_id}) added successfully!")
            return redirect('employee_list')
        except Exception as e:
            messages.error(request, f"Error: {e}")
    
    return render(request, 'employeeCRUD/employee_form.html')

# Edit employee
def employee_edit(request, id):
    emp = get_object_or_404(Employee, id=id)
    
    if request.method == "POST":
        try:
            emp.name = request.POST['name']
            emp.phone = request.POST['phone']
            emp.email = request.POST['email']
            emp.designation = request.POST['designation']
            emp.salary = request.POST['salary']
            emp.status = request.POST['status']
            emp.gender = request.POST['gender']
            emp.dob = request.POST['dob']
            emp.aadhaar = request.POST.get('aadhaar', '')
            emp.address = request.POST['address']
            emp.date_of_joining = request.POST['date_of_joining']
            
            if 'photo' in request.FILES:
                emp.photo = request.FILES['photo']
            emp.save()
            
            messages.success(request, f"Employee {emp.name} updated successfully!")
            return redirect('employee_list')
        except Exception as e:
            messages.error(request, f"Error: {e}")
    
    return render(request, 'employeeCRUD/employee_form.html', {'emp': emp})

# Delete employee
def employee_delete(request, id):
    emp = get_object_or_404(Employee, id=id)
    if request.method == "POST":
        emp.delete()
        messages.success(request, f"Employee {emp.name} deleted!")
        return redirect('employee_list')
    return render(request, 'employeeCRUD/employee_delete.html', {'emp': emp})


# student/views.py
def student_list(request):
    students = Student.objects.all()
    return render(request, 'studentCRUD/student_list.html', {'students': students})

def student_add(request):
    all_students = Student.objects.all()  # for joint select
    if request.method == "POST":
        try:
            student = Student(
                name=request.POST['name'],
                phone=request.POST['phone'],
                email=request.POST['email'],
                course=request.POST['course'],
                feePaid=request.POST.get('fee_paid', '0'),
                status=request.POST['status'],
                gender=request.POST['gender'],
                dob=request.POST['dob'],
                aadhaar=request.POST.get('aadhaar', ''),
                address=request.POST['address'],
                date_of_joining=request.POST['date_of_joining'],
            )
            if 'photo' in request.FILES:
                student.photo = request.FILES['photo']
            
            # Joint students handle
            student.joint_students = request.POST.getlist('joint_students')
            
            student.save()
            messages.success(request, f"Student {student.name} ({student.student_id}) enrolled!")
            return redirect('student_list')
        except Exception as e:
            messages.error(request, f"Error: {e}")
    
    return render(request, 'studentCRUD/student_form.html', {'all_students': all_students})

def student_edit(request, id):
    student = get_object_or_404(Student, id=id)
    all_students = Student.objects.exclude(id=id)
    if request.method == "POST":
        try:
            student.name = request.POST['name']
            student.phone = request.POST['phone']
            student.email = request.POST['email']
            student.course = request.POST['course']
            student.feePaid = request.POST.get('fee_paid', '0')
            student.status = request.POST['status']
            student.gender = request.POST['gender']
            student.dob = request.POST['dob']
            student.aadhaar = request.POST.get('aadhaar', '')
            student.address = request.POST['address']
            student.date_of_joining = request.POST['date_of_joining']
            student.joint_students = request.POST.getlist('joint_students')  # Updated
            if 'photo' in request.FILES:
                student.photo = request.FILES['photo']
            student.save()
            messages.success(request, "Student updated!")
            return redirect('student_list')
        except Exception as e:
            messages.error(request, f"Error: {e}")
    
    return render(request, 'studentCRUD/student_form.html', {'student': student, 'all_students': all_students})

def student_delete(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == "POST":
        student.delete()
        messages.success(request, "Student deleted!")
        return redirect('student_list')
    return render(request, 'studentCRUD/student_delete.html', {'student': student})