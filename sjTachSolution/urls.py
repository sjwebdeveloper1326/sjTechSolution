"""
URL configuration for sjTachSolution project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
# from sjTachSolution.sjTachSolution import views
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_page,name='home'),
    path('about/', views.about,name='about'),
    path('testimonial/', views.testimonial,name='testimonial'),
    path('courses/', views.courses,name='courses'),
    path('services_list/', views.services,name='services_list'),
    path('controller/', views.controller,name='controller'),
    path('enroll/', views.enroll_page, name='enroll_page'),
 # Add this line 👇
    path('pages/', include('mainApp.urls')),
    path('', include('employee_Client_student.urls')),
]

# Media files ke liye (photo upload)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)