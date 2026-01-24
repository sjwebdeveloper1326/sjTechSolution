from pyexpat.errors import messages
from django.shortcuts import render, redirect, get_object_or_404

from mainApp.models import Course, Enrollment, Service

def index_page(request):
    # services = Service.objects.all()
    return render(request, 'index.html')
    # return render(request, 'index.html', {'services': services})

def about(request):
    return render(request, 'about.html')

def testimonial(request):
    return render(request, 'testimonial.html')
   

# views.py

# from django.shortcuts import render, redirect
# from django.contrib import messages   # <-- YEH LINE HONA HI CHAHIYE

# def index_page(request):
#     # Sirf test ke liye message dikhana chahte ho toh yeh karo
#     messages.success(request, "Welcome to SJ.Tech Solution!")
#     messages.error(request, "Yeh error message hai")
#     messages.info(request, "Server is running smoothly")

#     return render(request, 'index.html')

def courses(request):
    return render(request, 'courses.html',)

def services(request):
    services = Service.objects.all()
    return render(request, 'service.html', {'services': services})

def courses(request):
    courses = Course.objects.filter()  # Sab courses
    context = {
        'courses': courses
    }
    return render(request, 'courses.html', context)

def controller(request):
    return render(request, 'controller.html',)


def enroll_page(request):
    courses = Course.objects.all()

    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        course = request.POST.get('course')

        # Simple duplicate check (optional)
        if Enrollment.objects.filter(phone=phone, course=course).exists():
            messages.warning(request, f"Arre {name}, tum already enroll ho chuke ho is course mein!")
        else:
            Enrollment.objects.create(
                name=name,
                phone=phone,
                email=email,
                course=course
            )
            messages.success(request, 
                f"Badhai ho {name}! Tumhara enrollment successful ho gaya hai 🔥 "
                "Hum jaldi hi WhatsApp pe batch details bhejenge!")
        
        return redirect('enroll_page')  # Prevent duplicate on refresh

    context = {'courses': courses}
    return render(request, 'enroll.html', context)

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