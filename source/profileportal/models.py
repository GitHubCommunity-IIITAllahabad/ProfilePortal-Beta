# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

#Model for user info
class StudentSite(models.Model):
	RollNo = models.CharField(max_length=20, default='', unique='True')
	CurrentSem = models.CharField(max_length=5, default='')
	name = models.CharField(max_length=50, default='')
	hackerearth = models.CharField(max_length=500, default='', blank=True)
	codechef = models.CharField(max_length=500, default='', blank=True)
	spoj = models.CharField(max_length=500, default='', blank=True)
	github = models.CharField(max_length=500, default='', blank=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated_on = models.DateTimeField(auto_now=True, auto_now_add=False)

	def __unicode__(self):
		return self.RollNo
