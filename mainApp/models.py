from django.db import models

class Service(models.Model):
    icon = models.CharField(max_length=100)   # example: "fas fa-laptop-code"
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title

# Courses CRUD start...
class Course(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    description = models.TextField()
    is_new = models.BooleanField(default=False, help_text="Check if 'NEW' badge dikhana hai")
    features = models.JSONField(default=list, help_text="Example: ['3 Months Live Training', '5+ Real Projects', 'Job Assistance']")
    order = models.PositiveIntegerField(default=0, help_text="Chhota number = pehle dikhega")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return self.title
# Courses CRUD end...

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