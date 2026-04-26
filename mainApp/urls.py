from django.contrib import admin
from django.urls import path

from mainApp.views.course_views import course_create, course_delete, course_list, course_update
from mainApp.views.payment_views import submit_payment
from mainApp.views.services_views import service_create, service_delete, service_list, service_update
from mainApp.views.project_views import add_project, delete_project, edit_project, projects_list
from mainApp.views.testimonial_views import add_testimonial, delete_testimonial, edit_testimonial, testimonial_list


# from sjTachSolution.sjTachSolution import views
from . import views
urlpatterns = [
     # Services CRUD
    path('services/', service_list, name='service_list'),
    path('services/create/', service_create, name='service_create'),
    path('services/update/<int:id>/', service_update, name='service_update'),
    path('services/delete/<int:id>/', service_delete, name='service_delete'),

    path("courses-list/", course_list, name="course_list"),
    path("courses/add/", course_create, name="course_create"),
    path("courses/edit/<int:pk>/", course_update, name="course_update"),
    path("courses/delete/<int:pk>/", course_delete, name="course_delete"),

    path("submit-payment/<int:course_id>/", submit_payment, name="submit_payment"),

    path('projects-list/', projects_list, name='projects_list'),
    path('add-project/', add_project, name='add_project'),
    path('edit-project/<int:id>/', edit_project, name='edit_project'),
    path('delete-project/<int:id>/', delete_project, name='delete_project'),
    
    path('testimonials/', testimonial_list, name='testimonial_list'),
    path('testimonials/add/', add_testimonial, name='add_testimonial'),
    path('testimonials/edit/<int:id>/', edit_testimonial, name='edit_testimonial'),
    path('testimonials/delete/<int:id>/', delete_testimonial, name='delete_testimonial'),\
        ]
