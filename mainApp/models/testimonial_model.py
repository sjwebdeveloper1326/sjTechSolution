from django.db import models

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=150)
    message = models.TextField()
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='testimonials/',blank=True, null=True)
    rating = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name