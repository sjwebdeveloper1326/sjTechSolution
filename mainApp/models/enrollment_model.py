from django.db import models
from datetime import datetime
# Student Enrollment
class Enrollment(models.Model):
    COURSE_CHOICES = [
        ('Full Stack Web Development', 'Full Stack Web Development'),
        ('Python & Data Science', 'Python & Data Science'),
        ('Digital Marketing Mastery', 'Digital Marketing Mastery'),
    ]

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    studentId = models.CharField(max_length=15)
    email = models.EmailField()
    course = models.CharField(max_length=100, choices=COURSE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)  # Admin dekh sake

    def __str__(self):
        return f"{self.name} - {self.course}"

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Enrollments"