from django.contrib import admin

from mainApp.models.contact_model import Contact, Newsletter
from mainApp.models.course_model import Course
from mainApp.models.enrollment_model import Enrollment
from mainApp.models.payment_model import Payment
from mainApp.models.service_model import Service
from mainApp.models.project_model import Project
# from .models import Course, Enrollment, Service

admin.site.register(Payment)
admin.site.register(Service)
admin.site.register(Newsletter)
admin.site.register(Contact)
admin.site.register(Project)
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_new', 'order', 'created_at')
    list_editable = ('order', 'is_new')
    list_per_page = 20
    search_fields = ('title', 'description')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'course', 'created_at', 'is_processed')
    list_filter = ('course', 'created_at')
    search_fields = ('name', 'phone', 'email','studentId')
    readonly_fields = ('created_at',)
    list_per_page = 25