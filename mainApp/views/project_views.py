from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from mainApp.forms import ProjectForm
from mainApp.models.project_model import Project
from django.core.paginator import Paginator

# READ (List)
def projects_list(request):
    if not request.user.is_authenticated:
        raise Http404()

    project_list = Project.objects.all().order_by('-id')

    paginator = Paginator(project_list, 5)  # 👈 5 per page
    page_number = request.GET.get('page')
    projects = paginator.get_page(page_number)

    return render(request, 'projectCRUD/project_list.html', {
        'projects': projects
    })

# CREATE
def add_project(request):
    if not request.user.is_authenticated:
        raise Http404()

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Project created successfully! ✔")
            return redirect('projects_list')
        else:
            messages.error(request, "Please fix the errors below ❌")
    else:
        form = ProjectForm()

    return render(request, 'projectCRUD/project_form.html', {'form': form})


# UPDATE
def edit_project(request, id):
    if not request.user.is_authenticated:
        raise Http404()

    project = get_object_or_404(Project, id=id)

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Project updated successfully! ✔")
            return redirect('projects_list')
        else:
            messages.error(request, "Please fix the errors below ❌")
    else:
        form = ProjectForm(instance=project)

    return render(request, 'projectCRUD/project_form.html', {'form': form})


# DELETE
def delete_project(request, id):
    if not request.user.is_authenticated:
        raise Http404()

    project = get_object_or_404(Project, id=id)
    project.delete()
    messages.success(request, "Project deleted successfully! 🗑️")
    return redirect('projects_list')