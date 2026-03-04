# from django.db import models
# from django.utils import timezone
# from django.contrib.auth.models import User
# from utils.account_helper import create_system_user
# from utils.loginMail_utils import send_account_email   
# import uuid

# class Employee(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
#     uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
#     emp_id = models.CharField(max_length=10, unique=True, blank=True)
#     name = models.CharField(max_length=100)
#     phone = models.CharField(max_length=15)
#     email = models.EmailField(unique=True)
#     photo = models.ImageField(upload_to='employees/', blank=True, null=True)
#     designation = models.CharField(max_length=100, blank=True)
#     salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     status = models.CharField(max_length=20, default='active', blank=True)
#     gender = models.CharField(max_length=10, blank=True)
#     dob = models.DateField(blank=True, null=True)
#     aadhaar = models.CharField(max_length=12, blank=True, null=True)
#     address = models.TextField(blank=True)
#     role = models.CharField(max_length=50, blank=True)
#     date_of_joining = models.DateField(blank=True, null=True)
#     state = models.CharField(max_length=100, blank=True)
#     city = models.CharField(max_length=100, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def save(self, *args, **kwargs):
#         creating = self.pk is None

#         # Auto emp_id
#         # if creating and not self.emp_id:
#         #     last = Employee.objects.order_by('-id').first()
#         #     num = last.id + 1 if last else 1
#         #     self.emp_id = f"SJE-{num:04d}"
#         if creating and not self.emp_id:
#           if self.role == "teacher":
#               prefix = "SJT"
#           elif self.role == "client":
#               prefix = "SJC"
#           else:
#               prefix = "SJE"

#         last = Employee.objects.filter(
#             emp_id__startswith=prefix
#         ).order_by('-id').first()

#         num = last.id + 1 if last else 1
#         self.emp_id = f"{prefix}-{num:04d}"

#         super().save(*args, **kwargs)

#         # Create user + send mail
#         if creating and not self.user:
#             user, username, plain_password = create_system_user(
#                 self.name,
#                 self.email,
#                 self.emp_id
#             )

#             self.user = user
#             super().save(update_fields=["user"])

#             print("Sending mail to:", self.email)  # DEBUG

#             try:
#                 send_account_email(
#                     to_email=self.email,
#                     name=self.name,
#                     username=username,
#                     password=plain_password
#                 )
#             except Exception as e:
#                 print("EMAIL FAILED:", e)

#     def __str__(self):
#         return f"{self.emp_id} - {self.name}"


# # # student Model
# class Student(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
#     uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
#     student_id = models.CharField(max_length=10, unique=True, blank=True)
#     name = models.CharField(max_length=100)
#     phone = models.CharField(max_length=15)
#     email = models.EmailField(unique=True)
#     photo = models.ImageField(upload_to='students/', blank=True, null=True)
#     course = models.CharField(max_length=100)
#     feePaid = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     status = models.CharField(max_length=20, default='active')
#     gender = models.CharField(max_length=10, default='male')
#     dob = models.DateField("Date of Birth")
#     aadhaar = models.CharField(max_length=12, blank=True, null=True)
#     address = models.TextField()
#     jointStudents = models.JSONField(default=list, blank=True)
#     date_of_joining = models.DateField(default=timezone.now)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def save(self, *args, **kwargs):
#         creating = self.pk is None

#         # Auto student_id
#         if creating and not self.student_id:
#             last = Student.objects.order_by('-id').first()
#             num = last.id + 1 if last else 1
#             self.student_id = f"SJS-{num:04d}"

#         super().save(*args, **kwargs)

#         # Create user + send mail
#         if creating and not self.user:
#             user, username, plain_password = create_system_user(
#                 self.name,
#                 self.email,
#                 self.student_id
#             )

#             self.user = user
#             super().save(update_fields=["user"])

#             try:
#                 send_account_email(
#                     to_email=self.email,
#                     name=self.name,
#                     username=username,
#                     password=plain_password
#                 )
#             except Exception as e:
#                 print("EMAIL FAILED:", e)

#     def __str__(self):
#         return f"{self.student_id} - {self.name}"
