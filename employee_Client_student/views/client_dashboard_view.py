from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render

from employee_Client_student.models.employee_model import Employee
from mainApp.models.project_model import Project
from mainApp.views.project_views import hydrate_project_assignments


@login_required(login_url='login')
def client_dashboard(request, emp_uuid):
    client = get_object_or_404(Employee, emp_uuid=emp_uuid, role='client')
    if client.user != request.user:
        return HttpResponseForbidden('You are not allowed to view this dashboard.')

    projects = list(Project.objects.filter(client_uuid=str(client.emp_uuid)).order_by('-created_at'))
    hydrate_project_assignments(projects)

    return render(request, 'clientCRUD/dashboard_client.html', {
        'client': client,
        'employee': client,
        'projects': projects,
        'profile_uuid': client.emp_uuid,
        'profile_id': client.emp_id,
        'user_type': 'client',
    })
