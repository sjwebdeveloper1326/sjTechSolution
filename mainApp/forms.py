from django import forms

from employee_Client_student.models.employee_model import Employee
from employee_Client_student.models.student_model import Student
from mainApp.models.service_model import Service
from mainApp.models.project_model import Project
from mainApp.models.testimonial_model import Testimonial
# from .models import Service


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['icon', 'title', 'description']


class ProjectForm(forms.ModelForm):
    client_uuid = forms.ChoiceField(
        label="Project Client",
        required=False,
        choices=[],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    assigned_employee_ids = forms.MultipleChoiceField(
        label="Handled By Employees",
        required=False,
        choices=[],
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'size': 6})
    )
    assigned_student_ids = forms.MultipleChoiceField(
        label="Handled By Students",
        required=False,
        choices=[],
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'size': 6})
    )

    class Meta:
        model = Project
        fields = [
            'title',
            'description',
            'image',
            'link',
            'client_uuid',
            'assigned_employee_ids',
            'assigned_student_ids',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        clients = Employee.objects.filter(role='client', status='active').order_by('name')
        employees = Employee.objects.exclude(role='client').filter(status='active').order_by('name')
        students = Student.objects.filter(status='active').order_by('name')

        self.fields['client_uuid'].choices = [('', '-- Select Client --')] + [
            (str(client.emp_uuid), f'{client.name} ({client.emp_id})')
            for client in clients
        ]
        self.fields['assigned_employee_ids'].choices = [
            (str(employee.emp_uuid), f'{employee.name} ({employee.emp_id})')
            for employee in employees
        ]
        self.fields['assigned_student_ids'].choices = [
            (str(student.stu_uuid), f'{student.name} ({student.student_id})')
            for student in students
        ]

        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
        self.fields['link'].widget.attrs.update({'class': 'form-control'})


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
