from django import forms

from mainApp.models.service_model import Service
from mainApp.models.project_model import Project
# from .models import Service

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['icon', 'title', 'description']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'image', 'link']