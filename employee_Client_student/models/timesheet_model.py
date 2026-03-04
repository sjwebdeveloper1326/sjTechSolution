import uuid
from django.db import models
from employee_Client_student.models.employee_model import Employee
import uuid
from django.db import models

class TimeSheet(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    employee = models.ForeignKey(
        "employee_Client_student.Employee", 
        on_delete=models.CASCADE,
        related_name="timesheets"
    )

    date = models.DateField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.emp_id} - {self.date}"