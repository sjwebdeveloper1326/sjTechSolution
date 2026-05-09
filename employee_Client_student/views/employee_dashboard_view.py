import uuid

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from employee_Client_student.models import Employee, Student
from mainApp.models.course_model import Course
from mainApp.models.project_model import Project
from mainApp.views.project_views import hydrate_project_assignments


# def employee_dashboard(request, emp_uuid):
#     employee = get_object_or_404(Employee, emp_uuid=emp_uuid, user=request.user)
    
#     timesheets = employee.timesheets.all().order_by('-date')
    
#     str_uuid = str(employee.emp_uuid)
    
#     print("\n" + "="*60)
#     print(f"DEBUG: Employee Dashboard - {employee.name} ({employee.role})")
#     print(f"DEBUG: emp_uuid = {str_uuid}")
#     print("="*60 + "\n")
    
#     my_students = []
    
#     if employee.role.lower() in ["teacher", "instructor", "trainer"]:
#         teacher_course_ids = []
        
#         for course in Course.objects.all():
#             if isinstance(course.teacher_ids, list) and str_uuid in course.teacher_ids:
#                 if course.course_id:
#                     teacher_course_ids.append(course.course_id)
#                     print(f"Matched Course: {course.title} ({course.course_id})")
#                 else:
#                     print(f"WARNING: Course '{course.title}' (ID: {course.id}) ka course_id None hai – ignore kar rahe")
        
#         print(f"DEBUG: Valid matched course_ids = {teacher_course_ids}")
        
#         if teacher_course_ids:
#             for student in Student.objects.all():
#                 student_course_ids = student.course_ids or []
#                 if any(cid in student_course_ids for cid in teacher_course_ids):
#                     my_students.append(student)
#                     print(f"MATCHED → {student.student_id} | {student.name} | courses: {student_course_ids}")
        
#         print(f"DEBUG: Total matched students = {len(my_students)}")
    
#     context = {
#         "employee": employee,
#         "timesheets": timesheets,
#         "my_students": my_students,
#         "profile_uuid": employee.emp_uuid,
#         "profile_id": employee.emp_id,
#         "user_type": "employee",
#         "emp_uuid": employee.emp_uuid,
#     }
#     return render(request, "employeeCRUD/dashboard_employee.html", context)
@login_required(login_url='login')
def employee_dashboard(request, emp_uuid):
    employee = get_object_or_404(Employee, emp_uuid=emp_uuid, user=request.user)
    
    timesheets = employee.timesheets.all().order_by('-date')
    
    str_uuid = str(employee.emp_uuid)  # UUID ko string mein convert
    
    print("\n" + "="*80)
    print(f"EMPLOYEE DASHBOARD DEBUG → {employee.name} ({employee.role}) | UUID: {str_uuid}")
    print("="*80 + "\n")
    
    # 1. My Students (teachers ke liye – course PK se match)
    my_students = []
    if employee.role.lower() in ["teacher", "instructor", "trainer"]:
        teacher_course_pks = []
        
        for course in Course.objects.all():
            teacher_list = course.teacher_ids or []
            if isinstance(teacher_list, list) and str_uuid in teacher_list:
                teacher_course_pks.append(course.pk)
                print(f"✓ Matched Course for Students: {course.title} → PK: {course.pk}")
        
        print(f"\nTeacher ke matched course PKs = {teacher_course_pks}")
        
        if teacher_course_pks:
            for student in Student.objects.all():
                student_course_ids = student.course_ids or []
                if any(int(cid) in teacher_course_pks for cid in student_course_ids if cid):
                    my_students.append(student)
                    print(f"STUDENTS MATCHED: {student.student_id} | {student.name} | courses: {student_course_ids}")
        
        print(f"Total my_students = {len(my_students)}")
    
    # 2. Referrals Members – jointBy se match (sabke liye show)
    referrals = []
    for student in Student.objects.all():
        joint_by_value = student.jointBy
        
        # jointBy JSONField hai – string ya list ho sakta hai
        if isinstance(joint_by_value, str) and str_uuid == joint_by_value:
            referrals.append(student)
            print(f"REFERRAL MATCH (str): {student.student_id} | {student.name} | jointBy: {joint_by_value}")
        
        elif isinstance(joint_by_value, list) and str_uuid in joint_by_value:
            referrals.append(student)
            print(f"REFERRAL MATCH (list): {student.student_id} | {student.name} | jointBy: {joint_by_value}")
    
    # newest first sort
    referrals.sort(key=lambda s: s.date_of_joining or timezone.now(), reverse=True)
    
    print(f"\nTotal referrals (jointBy match) = {len(referrals)}")
    
    assigned_projects = []
    for project in Project.objects.all().order_by('-created_at'):
        if str_uuid in (project.assigned_employee_ids or []):
            assigned_projects.append(project)

    hydrate_project_assignments(assigned_projects)

    context = {
        "employee": employee,
        "timesheets": timesheets,
        "my_students": my_students,
        "referrals": referrals,  # ← ab yeh referrals tab mein jayega
        "assigned_projects": assigned_projects,
        "profile_uuid": employee.emp_uuid,
        "profile_id": employee.emp_id,
        "user_type": "employee",
        "emp_uuid": employee.emp_uuid,
    }
    return render(request, "employeeCRUD/dashboard_employee.html", context)
