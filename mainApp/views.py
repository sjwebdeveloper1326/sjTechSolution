from django.shortcuts import get_object_or_404, redirect, render

from mainApp.forms import ServiceForm
from .models import Course, Service
from django.contrib import messages

# Service CRUD Start....
def service_list(request):
    services = Service.objects.all()
    return render(request, 'serviceCRUD/service_list.html', {'services': services})


# CREATE
def service_create(request):
    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Service created successfully! ✔")
            return redirect("service_list")
        else:
            messages.error(request, "Please fix the errors below ❌")
    else:
        form = ServiceForm()

    return render(request, "serviceCRUD/service_form.html", {"form": form})


# UPDATE
def service_update(request, id):
    service = get_object_or_404(Service, id=id)

    if request.method == "POST":
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, "Service updated successfully! ✔")
            return redirect("service_list")
        else:
            messages.error(request, "Please fix the errors below ❌")
    else:
        form = ServiceForm(instance=service)

    return render(request, 'serviceCRUD/service_form.html', {'form': form})


# DELETE
def service_delete(request, id):
    service = get_object_or_404(Service, id=id)
    service.delete()
    messages.success(request, "Service deleted successfully! 🗑️")
    return redirect('service_list')


# Service CRUD End....

# Cources CRUD start...
def courses_page(request):
    courses = Course.objects.filter()  # Sab courses
    context = {
        'courses': courses
    }
    return render(request, 'courses.html', context)
# Cources CRUD end...