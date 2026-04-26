from django import forms

from mainApp.models.service_model import Service
from mainApp.models.project_model import Project
from mainApp.models.testimonial_model import Testimonial
# from .models import Service


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['icon', 'title', 'description']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'image', 'link']


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'designation', 'email', 'message', 'image', 'rating']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'}),
            'designation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter designation'}),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email',
                'required': 'required'
            }),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter message'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter rating'}),
        }
