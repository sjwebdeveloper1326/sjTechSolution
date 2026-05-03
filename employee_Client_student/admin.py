from django.contrib import admin

from employee_Client_student.models import Employee, Student



@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("emp_id", "name", "email", "role", "status")
    list_filter = ("role", "status")
    search_fields = ("name", "email", "emp_id")

    fieldsets = (
        ("Basic Info", {
            "fields": ("name", "email", "phone", "photo")
        }),
        ("Job Details", {
            "fields": ("role", "designation", "salary", "status")
        }),
        ("Personal Info", {
            "fields": ("gender", "dob", "aadhaar", "address", "state", "city")
        }),
        ("System Info", {
            "fields": ("emp_id", "emp_uuid", "user"),
        }),
    )

    readonly_fields = ("emp_id", "emp_uuid", "user")
admin.site.register(Student)
# Register your models here.
