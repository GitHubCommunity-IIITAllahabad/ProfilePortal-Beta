# -*- coding: utf-8 -*-
#admin username: softdev
#admin password: softdev123
from __future__ import unicode_literals

from django.contrib import admin
from .models import StudentSite
from .forms import StudentSiteForm

# Register your models here.
class StudentSiteAdmin(admin.ModelAdmin):
	list_display = ["__unicode__","timestamp","updated_on"]
	form = StudentSiteForm
	#class Meta:
	#	model = StudentSite

admin.site.register(StudentSite,StudentSiteAdmin)
