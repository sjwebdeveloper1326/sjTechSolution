from django.contrib import admin
from django.urls import path

# from sjTachSolution.sjTachSolution import views
from . import views
urlpatterns = [
     # Services CRUD
    path('services/', views.service_list, name='service_list'),
    path('services/create/', views.service_create, name='service_create'),
    path('services/update/<int:id>/', views.service_update, name='service_update'),
    path('services/delete/<int:id>/', views.service_delete, name='service_delete'),
]
