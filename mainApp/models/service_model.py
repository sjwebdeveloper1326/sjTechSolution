from django.db import models

class Service(models.Model):
    icon = models.CharField(max_length=100)   # example: "fas fa-laptop-code"
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title
