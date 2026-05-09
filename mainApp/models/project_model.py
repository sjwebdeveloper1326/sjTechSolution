from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/')
    link = models.URLField(blank=True, null=True)
    client_uuid = models.CharField(max_length=36, blank=True, null=True)
    assigned_employee_ids = models.JSONField(default=list, blank=True)
    assigned_student_ids = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
