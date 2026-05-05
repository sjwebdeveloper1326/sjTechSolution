from django.shortcuts import get_object_or_404, redirect, render

from mainApp.forms import ServiceForm
from django.contrib import messages

from employee_Client_student.decorators import admin_level_required
from mainApp.models.service_model import Service

# from mainApp.models import Service

# Service CRUD Start....
@admin_level_required
def service_list(request):
    services = Service.objects.all()
    return render(request, 'serviceCRUD/service_list.html', {'services': services})


# CREATE
@admin_level_required
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
@admin_level_required
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
@admin_level_required
def service_delete(request, id):
    service = get_object_or_404(Service, id=id)
    service.delete()
    messages.success(request, "Service deleted successfully! 🗑️")
    return redirect('service_list')


# Service CRUD End....
