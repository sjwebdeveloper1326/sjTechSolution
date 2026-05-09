from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from mainApp.forms import ProjectForm
from mainApp.models.project_model import Project
from django.core.paginator import Paginator
from employee_Client_student.decorators import admin_level_required
from employee_Client_student.models.employee_model import Employee
from employee_Client_student.models.student_model import Student


def hydrate_project_assignments(projects):
    client_ids = [project.client_uuid for project in projects if project.client_uuid]
    employee_ids = []
    student_ids = []

    for project in projects:
        employee_ids.extend(project.assigned_employee_ids or [])
        student_ids.extend(project.assigned_student_ids or [])

    clients = {
        str(client.emp_uuid): client
        for client in Employee.objects.filter(emp_uuid__in=client_ids)
    }
    employees = {
        str(employee.emp_uuid): employee
        for employee in Employee.objects.filter(emp_uuid__in=employee_ids)
    }
    students = {
        str(student.stu_uuid): student
        for student in Student.objects.filter(stu_uuid__in=student_ids)
    }

    for project in projects:
        project.client = clients.get(project.client_uuid)
        project.assigned_employees = [
            employees[emp_uuid]
            for emp_uuid in (project.assigned_employee_ids or [])
            if emp_uuid in employees
        ]
        project.assigned_students = [
            students[stu_uuid]
            for stu_uuid in (project.assigned_student_ids or [])
            if stu_uuid in students
        ]

    return projects

# READ (List)
@admin_level_required
def projects_list(request):
    project_list = Project.objects.all().order_by('-id')

    paginator = Paginator(project_list, 5)  # 👈 5 per page
    page_number = request.GET.get('page')
    projects = paginator.get_page(page_number)
    hydrate_project_assignments(projects.object_list)

    return render(request, 'projectCRUD/project_list.html', {
        'projects': projects
    })

# CREATE
@admin_level_required
def add_project(request):
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
@admin_level_required
def edit_project(request, id):
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
@admin_level_required
def delete_project(request, id):
    project = get_object_or_404(Project, id=id)
    project.delete()
    messages.success(request, "Project deleted successfully! 🗑️")
    return redirect('projects_list')
