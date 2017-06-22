from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Student, StudentSite, Site

class UserForm(forms.ModelForm):   
    class Meta:
        model = User
        fields = ['username','email','password']

class StudentForm(forms.ModelForm):   
    class Meta:
        model = Student
        fields = ['enrollment_no','first_name','last_name','current_semester','graduation_year','image']
        

class StudentSiteForm(forms.ModelForm):   
    class Meta:
        model = StudentSite
        fields = ['site','username','is_active']
