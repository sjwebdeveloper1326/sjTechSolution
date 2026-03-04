from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from employee_Client_student.models.employee_model import Employee
from employee_Client_student.models.timesheet_model import TimeSheet

def timesheet_add(request, emp_uuid):
    employee = get_object_or_404(Employee, emp_uuid=emp_uuid)

    if request.method == "POST":
        TimeSheet.objects.create(
            employee=employee,
            date=request.POST.get('date'),
            check_in=request.POST.get('check_in'),
            check_out=request.POST.get('check_out'),
            hours=request.POST.get('hours'),
            description=request.POST.get('description'),
        )

        messages.success(request, "Timesheet added successfully")
        return redirect('dashboard_employee', emp_uuid=employee.emp_uuid)

    return render(request, 'partials/timesheet_form.html', {
        'employee': employee,
        'action': 'Add',
        'emp_uuid': emp_uuid,
    })

def timesheet_edit(request, emp_uuid, ts_uuid):
    employee = get_object_or_404(Employee, emp_uuid=emp_uuid)
    timesheet = get_object_or_404(TimeSheet, uuid=ts_uuid, employee=employee)

    if request.method == "POST":
        timesheet.date = request.POST.get('date')
        timesheet.check_in = request.POST.get('check_in')
        timesheet.check_out = request.POST.get('check_out')
        timesheet.hours = request.POST.get('hours')
        timesheet.description = request.POST.get('description')
        timesheet.save()

        messages.success(request, "Timesheet updated")
        return redirect('dashboard_employee', emp_uuid=employee.emp_uuid)

    return render(request, 'partials/timesheet_form.html', {
        'employee': employee,
        'timesheet': timesheet,
        'action': 'Edit'
    })

def timesheet_delete(request, emp_uuid, ts_uuid):
    employee = get_object_or_404(Employee, emp_uuid=emp_uuid)
    timesheet = get_object_or_404(TimeSheet, uuid=ts_uuid, employee=employee)

    timesheet.delete()
    messages.success(request, "Timesheet deleted")

    return redirect('dashboard_employee', emp_uuid=employee.emp_uuid)


def timesheet_list(request, emp_uuid):
    employee = get_object_or_404(Employee, emp_uuid=emp_uuid)
    timesheets = employee.timesheets.all().order_by('-date')

    return render(request, 'employeeCRUD/dashboard_employee.html', {
        'employee': employee,
        'timesheets': timesheets,
    })