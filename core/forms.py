from . import models
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):
    class Meta:
        model = models.User
        fields = ['name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter email'})
        self.fields['name'].widget.attrs.update({'placeholder': 'Enter name'})
        

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ["first_name", "last_name", "email"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }
        

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = models.Appointment
        fields = ['name', 'email', 'phone', 'date', 'department', 'doctor', 'message']
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "format": "%Y-%m-%d"}),
        }

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.fields['department'].queryset = models.Department.objects.all()
        self.fields['doctor'].queryset = models.Doctor.objects.none()

        if 'department' in self.data:
            try:
                department_id = int(self.data.get('department'))
                self.fields['doctor'].queryset = models.Doctor.objects.filter(department_id=department_id)
            except (ValueError, TypeError):
                pass 
        elif self.instance.pk and self.instance.department:
            self.fields['doctor'].queryset = self.instance.department.doctors.all() 
        
        
class ContactForm(ModelForm):
    class Meta:
        model = models.ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        

