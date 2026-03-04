
from django.urls import path
from django.contrib.auth import views as auth_views

# auth
from employee_Client_student.views import employee_dashboard_view
from employee_Client_student.views.auth_views import login_view, logout_view

# password
from employee_Client_student.views.password_reset_views import (
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView,
    register_view,
)

# employee
from employee_Client_student.views.employee_dashboard_view import employee_dashboard
from employee_Client_student.views.employee_views import (
    employee_add, employee_edit, employee_delete, employee_list
)

# student
from employee_Client_student.views.student_dashboard_view import student_dashboard
from employee_Client_student.views.student_views import (
    student_add, student_edit, student_list
)
from employee_Client_student.views.timesheet_views import timesheet_add, timesheet_delete, timesheet_edit, timesheet_list
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
     path('login/', login_view, name="login"),
     path('logout/',logout_view, name='logout'),
     
     path(
    'password-reset/',
    views.CustomPasswordResetView.as_view(
        success_url='/login/'   
    ),
    name='password_reset'
      ),
#     path(
#     'password-reset/',
#     views.CustomPasswordResetView.as_view(),
#     name='password_reset'
# ),

path(
    'password-reset/done/',
    auth_views.PasswordResetDoneView.as_view(
        template_name='auth/password_reset_done.html'
    ),
    name='password_reset_done'
),
#  forgot password start...

    # path('reset/<uidb64>/<token>/',
    #      auth_views.PasswordResetConfirmView.as_view(
    #          template_name='auth/password_reset_confirm.html',
    #          success_url='/reset/done/'
    #      ),
    #      name='password_reset_confirm'),
    path(
    'reset/<uidb64>/<token>/',
    CustomPasswordResetConfirmView.as_view(),
    name='password_reset_confirm'
),


    path(
    'reset/done/',
    views.CustomPasswordResetCompleteView.as_view(),
    name='password_reset_complete'
),
    #  forgot password end...

   # Register page
    path('register/', register_view, name="register"),
    #  path('profile/', views.profile_page, name='profile_page'),

    #  path("employee/dashboard/<uuid:uuid>/", employee_dashboard, name="dashboard_employee"),
     path(
    "employee/dashboard/<uuid:emp_uuid>/",
    employee_dashboard,
    name="dashboard_employee"
),
    #  path("employee/dashboard/<str:student_id>/", views.dashboard_employee, name="dashboard_employee"),
    path('student/dashboard/<str:student_id>/', student_dashboard, name="dashboard_student"),

    path('employees', employee_list, name='employee_list'),
    path('employees/add/', employee_add, name='employee_add'),
    path('employees/edit/<uuid:emp_uuid>/', employee_edit, name='employee_edit'),
    path('employees/delete/<uuid:emp_uuid>/', employee_delete, name='employee_delete'),
    
    path('students', student_list, name='student_list'),
    path('students/add/', student_add, name='student_add'),
    path('students/edit/<int:id>/', student_edit, name='student_edit'),
    # path('students/delete/<int:id>/', views.student_delete, name='student_delete'),

    path(
        'employee/<uuid:emp_uuid>/timesheet/',
        employee_dashboard,
        name='timesheet_list'
    ),

    path(
        'employee/<uuid:emp_uuid>/timesheet/add/',
        timesheet_add,
        name='timesheet_add'
    ),

    path(
        'employee/<uuid:emp_uuid>/timesheet/edit/<uuid:ts_uuid>/',
        timesheet_edit,
        name='timesheet_edit'
    ),

    path(
        'employee/<uuid:emp_uuid>/timesheet/delete/<uuid:ts_uuid>/',
        timesheet_delete,
        name='timesheet_delete'
    ),
]