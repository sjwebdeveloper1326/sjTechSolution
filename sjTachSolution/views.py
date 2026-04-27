
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from employee_Client_student.models.employee_model import Employee
from mainApp.models.contact_model import Contact, Newsletter
from mainApp.models.course_model import Course
from mainApp.models.enrollment_model import Enrollment
from mainApp.models.service_model import Service
from django.contrib.auth.decorators import login_required

from mainApp.models.project_model import Project
from mainApp.models.testimonial_model import Testimonial

# from mainApp.models import Course, Enrollment, Service

def index_page(request):
    projects = Project.objects.all().order_by('-id')
    testimonials = Testimonial.objects.filter(isaccepted=True).order_by("-id")[:10]
    # services = Service.objects.all()
    return render(request, 'index.html', {'projects': projects, "testimonials": testimonials})
    # return render(request, 'index.html', {'services': services})

def about(request):
    return render(request, 'about.html')

def testimonial(request):
    testimonials = Testimonial.objects.filter(isaccepted=True).order_by('-id')[:10]
    return render(request, 'testimonial.html', {
        'testimonials': testimonials
    })
    
def projects(request):
    projects = Project.objects.all().order_by('-id')
    return render(request, 'projects.html', {'projects': projects})
   

# views.py

# from django.shortcuts import render, redirect
# from django.contrib import messages   # <-- YEH LINE HONA HI CHAHIYE

# def index_page(request):
#     # Sirf test ke liye message dikhana chahte ho toh yeh karo
#     messages.success(request, "Welcome to SG.Automix Tech!")
#     messages.error(request, "Yeh error message hai")
#     messages.info(request, "Server is running smoothly")

#     return render(request, 'index.html')

# def courses(request):
#     return render(request, 'courses.html',)

def services(request):
    services = Service.objects.all()
    return render(request, 'service.html', {'services': services})

def courses(request):
    courses = Course.objects.filter()  # Sab courses
    context = {
        'courses': courses
    }
    return render(request, 'courses.html', context)

# @login_required(login_url='login')
# def controller(request):
#     return render(request, 'controller.html',)
@login_required(login_url='login')
# def controller(request):

#     try:
#         username = request.user.username
#         emp_id = username.split("@")[-1]
#         emp = Employee.objects.get(emp_id=emp_id)

#         if emp.role not in ["manager", "account-manager", "admin"]:
#             messages.error(request, "You do not have permission to access this page.")
#             return redirect("login")

#     except Employee.DoesNotExist:
#         messages.error(request, "Unauthorized access.")
#         return redirect("login")

#     return render(request, "controller.html")

# @login_required(login_url='login')
def controller(request):

    try:
        emp_id = request.user.username.split("@")[-1]
        emp = Employee.objects.get(emp_id=emp_id)

        allowed_roles = ["admin", "manager", "account-manager"]

        if emp.role not in allowed_roles:
            messages.error(request, "Permission denied.")
            return redirect("home")

    except Employee.DoesNotExist:
        messages.error(request, "Unauthorized access.")
        return redirect("login")

    return render(request, "controller.html")

def contact(request):

    if request.method == "POST":

        # NEWSLETTER FORM
        if "newsletter_email" in request.POST:

            email = request.POST.get("newsletter_email")

            if not email:
                messages.error(request, "Please enter a valid email address.")
                return redirect("contact")

            try:
                if Newsletter.objects.filter(email=email).exists():
                    messages.warning(request, "This email is already subscribed.")
                else:
                    Newsletter.objects.create(email=email)
                    messages.success(
                        request,
                        "🎉 Congratulations! You have successfully subscribed to our newsletter.",
                    )

            except Exception:
                messages.error(request, "Something went wrong. Please try again.")

            return redirect("contact")

        # CONTACT FORM
        if "first_name" in request.POST:

            first = request.POST.get("first_name")
            last = request.POST.get("last_name")
            email = request.POST.get("email")
            phone = request.POST.get("phone")
            message = request.POST.get("message")

            if not first or not email or not message:
                messages.error(request, "Please fill all required fields.")
                return redirect("contact")

            try:
                Contact.objects.create(
                    first_name=first,
                    last_name=last,
                    email=email,
                    phone=phone,
                    message=message,
                )

                messages.success(
                    request,
                    "🎉 Congratulations! Your message has been sent successfully. We will contact you soon."
                )

            except Exception:
                messages.error(request, "Something went wrong. Please try again later.")

            return redirect("contact")

    return render(request, "contact.html")


# def enroll_page(request):
#     courses = Course.objects.all()

#     if request.method == "POST":
#         name = request.POST.get('name')
#         phone = request.POST.get('phone')
#         email = request.POST.get('email')
#         course = request.POST.get('course')

#         # Simple duplicate check (optional)
#         if Enrollment.objects.filter(phone=phone, course=course).exists():
#             messages.warning(request, f"Arre {name}, tum already enroll ho chuke ho is course mein!")
#         else:
#             Enrollment.objects.create(
#                 name=name,
#                 phone=phone,
#                 email=email,
#                 course=course
#             )
#             messages.success(request, 
#                 f"Badhai ho {name}! Tumhara enrollment successful ho gaya hai 🔥 "
#                 "Hum jaldi hi WhatsApp pe batch details bhejenge!")
        
#         return redirect('enroll_page')  # Prevent duplicate on refresh

#     context = {'courses': courses}
#     return render(request, 'enroll.html', context)

# views.py
def enroll_page(request):
    courses = Course.objects.all()

    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        course = request.POST.get('course')

        if Enrollment.objects.filter(phone=phone, course=course).exists():
            messages.warning(request, "Already enrolled!")
        else:
            Enrollment.objects.create(name=name, phone=phone, email=email, course=course)
            messages.success(request, f"Success {name}! Enrollment complete!")

        return redirect('enroll_page')  # ← yahi URL name use hoga

    return render(request, 'enroll.html', {'courses': courses})

def custom_404(request, exception):
    return render(request, "404.html", status=404)
