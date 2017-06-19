from django import forms
from .models import StudentSite
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	class Meta: 
		model = User
		fields = ['username','email','password']

class StudentSiteForm(forms.ModelForm):
	class Meta:
		model = StudentSite
		exclude = []

	def clean_RollNo(self):
		RollNo = self.cleaned_data.get('RollNo')
		#enter condition:
		#(SAMPLE):
		#email_name,provider = email.split('@')
		#domain,extension = provider.split('.')
		#if not extension == "com"
		## (or)
		#if not "com" in email:
		#	raise forms.ValidationError("Please enter a valid .com address")
		return RollNo

	def clean_CurrentSem(self):
		CurrentSem = self.cleaned_data.get('CurrentSem')
		#Enter Condition if necessary
		return CurrentSem

	def clean_name(self):
		name = self.cleaned_data.get('name')
		#Enter Condition if necessary
		return name

	def clean_hackerearth(self):
		hackerearth = self.cleaned_data.get('hackerearth')
		#Enter Condition if necessary
		return hackerearth

	def clean_codechef(self):
		codechef = self.cleaned_data.get('codechef')
		#Enter Condition if necessary
		return codechef

	def clean_spoj(self):
		spoj = self.cleaned_data.get('spoj')
		#Enter Condition if necessary
		return spoj

	def clean_github(self):
		github = self.cleaned_data.get('github')
		#Enter Condition if necessary
		return github



