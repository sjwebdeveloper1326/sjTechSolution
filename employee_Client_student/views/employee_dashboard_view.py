import time
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from employee_Client_student.models import Employee, Student
from mainApp.models.course_model import Course
from mainApp.models.project_model import Project
from mainApp.views.project_views import hydrate_project_assignments
from utils.logger import get_page_logger, log_exception, log_info, log_warning


@login_required(login_url='login')
def employee_dashboard(request, emp_uuid):
    start_time = time.time()
    page_logger = get_page_logger('employee_dashboard')

    try:
        employee = get_object_or_404(Employee, emp_uuid=emp_uuid, user=request.user)

        timesheets = employee.timesheets.all().order_by('-date')

        str_uuid = str(employee.emp_uuid) if getattr(employee, 'emp_uuid', None) else ""

        page_logger.info(f"Employee dashboard opened for {employee.name} role={getattr(employee, 'role', '')} uuid={str_uuid} [user={request.user.username if getattr(request, 'user', None) else 'anonymous'}]")

        # 1. My Students (for teacher roles)
        my_students = []
        role = (getattr(employee, 'role', '') or '').lower()
        if role in ["teacher", "instructor", "trainer"]:
            teacher_course_pks = []
            for course in Course.objects.all():
                teacher_list = getattr(course, 'teacher_ids', None) or []
                # teacher_list may be a list or string; handle both
                if isinstance(teacher_list, list):
                    if str_uuid in teacher_list:
                        teacher_course_pks.append(course.pk)
                        page_logger.info(f"Matched course for teacher: {course.pk}")
                elif isinstance(teacher_list, str):
                    if str_uuid == teacher_list:
                        teacher_course_pks.append(course.pk)
                        page_logger.info(f"Matched course for teacher (str): {course.pk}")

            if teacher_course_pks:
                for student in Student.objects.all():
                    student_course_ids = getattr(student, 'course_ids', None) or []
                    if isinstance(student_course_ids, str):
                        # skip unsafe string formats
                        continue
                    for cid in student_course_ids:
                        try:
                            cid_int = int(cid)
                        except Exception:
                            continue
                        if cid_int in teacher_course_pks:
                            my_students.append(student)
                            break

        # 2. Referrals - match by jointBy (JSONField can be str/list/None)
        referrals = []
        for student in Student.objects.all():
            joint_by_value = getattr(student, 'jointBy', None)
            if isinstance(joint_by_value, str):
                if joint_by_value == str_uuid:
                    referrals.append(student)
            elif isinstance(joint_by_value, list):
                if str_uuid in joint_by_value:
                    referrals.append(student)

        # newest first
        referrals.sort(key=lambda s: s.date_of_joining or timezone.now(), reverse=True)

        assigned_projects = []
        for project in Project.objects.all().order_by('-created_at'):
            assigned = getattr(project, 'assigned_employee_ids', None) or []
            if isinstance(assigned, list) and str_uuid in assigned:
                assigned_projects.append(project)

        hydrate_project_assignments(assigned_projects)

        context = {
            "employee": employee,
            "timesheets": timesheets,
            "my_students": my_students,
            "referrals": referrals,
            "assigned_projects": assigned_projects,
            "profile_uuid": employee.emp_uuid,
            "profile_id": employee.emp_id,
            "user_type": "employee",
            "emp_uuid": employee.emp_uuid,
        }
        return render(request, "employeeCRUD/dashboard_employee.html", context)

    except Exception as exc:
        # Log the exception with request context and show friendly message
        try:
            log_exception(exc, request=request, module=__name__)
        except Exception:
            page_logger.error("Failed to log exception")
        messages.error(request, "An error occurred while preparing the dashboard. The issue has been reported.")
        return redirect('/')

    finally:
        # timing and slow request warning
        try:
            duration = time.time() - start_time
            page_logger.info(f"employee_dashboard duration={duration:.3f}s")
            slow_threshold =  getattr(__import__('django.conf').conf.settings, 'SLOW_REQUEST_THRESHOLD', 1.0)
            if duration > slow_threshold:
                log_warning(f"Slow page render: {duration:.3f}s", request=request, module=__name__)
        except Exception:
            pass
