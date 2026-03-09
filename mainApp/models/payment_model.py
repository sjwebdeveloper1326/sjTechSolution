from django.db import models
from datetime import datetime
import uuid

from employee_Client_student.models.student_model import Student
from mainApp.models.course_model import Course

class Payment(models.Model):
    pay_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)

    course = models.ForeignKey(Course,on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=8,decimal_places=2)

    message = models.TextField(blank=True,null=True)

    screenshot = models.ImageField(upload_to="payments/")

    status = models.CharField(max_length=20,default="pending")

    created_at = models.DateTimeField(auto_now_add=True)