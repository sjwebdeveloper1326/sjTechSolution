from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
     path('login/', views.login_view, name="login"),
     path('logout/', views.logout_view, name='logout'),
     
     path(
    'password-reset/',
    views.CustomPasswordResetView.as_view(
        success_url='/login/'   
    ),
    name='password_reset'
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
    views.CustomPasswordResetConfirmView.as_view(),
    name='password_reset_confirm'
),


    path(
    'reset/done/',
    views.CustomPasswordResetCompleteView.as_view(),
    name='password_reset_complete'
),
    #  forgot password end...

   # Register page
    path('register/', views.register_view, name="register"),
    #  path('profile/', views.profile_page, name='profile_page'),

     path("employee/dashboard/<str:emp_id>/", views.dashboard_employee, name="dashboard_employee"),
    #  path("employee/dashboard/<str:student_id>/", views.dashboard_employee, name="dashboard_employee"),
    path('student/dashboard/<str:student_id>/', views.dashboard_student, name="dashboard_student"),

    path('employees', views.employee_list, name='employee_list'),
    path('employees/add/', views.employee_add, name='employee_add'),
    path('employees/edit/<int:id>/', views.employee_edit, name='employee_edit'),
    path('employees/delete/<int:id>/', views.employee_delete, name='employee_delete'),
    
    path('students', views.student_list, name='student_list'),
    path('students/add/', views.student_add, name='student_add'),
    path('students/edit/<int:id>/', views.student_edit, name='student_edit'),
    path('students/delete/<int:id>/', views.student_delete, name='student_delete'),
]