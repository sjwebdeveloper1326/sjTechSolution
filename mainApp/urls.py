from django.contrib import admin
from django.urls import path

from mainApp.views.course_views import course_create, course_delete, course_list, course_update
from mainApp.views.payment_views import submit_payment
from mainApp.views.services_views import service_create, service_delete, service_list, service_update


# from sjTachSolution.sjTachSolution import views
from . import views
urlpatterns = [
     # Services CRUD
    path('services/', service_list, name='service_list'),
    path('services/create/', service_create, name='service_create'),
    path('services/update/<int:id>/', service_update, name='service_update'),
    path('services/delete/<int:id>/', service_delete, name='service_delete'),

    path("courses/", course_list, name="course_list"),
    path("courses/add/", course_create, name="course_create"),
    path("courses/edit/<int:pk>/", course_update, name="course_update"),
    path("courses/delete/<int:pk>/", course_delete, name="course_delete"),

   path("submit-payment/<int:course_id>/", submit_payment, name="submit_payment"),
]
