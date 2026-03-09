from django import forms

from mainApp.models.service_model import Service
# from .models import Service

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['icon', 'title', 'description']
