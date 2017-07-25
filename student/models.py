# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

#Model for user info
class Student(models.Model):
    user = models.ForeignKey(User,default=None,null=True)
    enrollment_no = models.CharField(max_length=50, default=None, unique=True)
    first_name = models.CharField(max_length=200, default=None)
    last_name = models.CharField(max_length=200, default=None)
    email = models.EmailField(default=None,null=True)
    current_semester = models.IntegerField(default=1, null=True)
    graduation_year = models.IntegerField(null=True)
    is_active = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    #image = models.FileField(blank=True, null=True)

    def __unicode__(self):
        return unicode(self.user)

    def __str__(self):
        return self.user

class Site(models.Model):
    
    site_type = models.CharField(max_length=100, default=None)
    site_name = models.CharField(max_length=200, default=None)
    site_active = models.BooleanField(default=False)
    site_count = models.IntegerField(default=0)

    def __str__(self):
        return self.site_name

class StudentSite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=None,null=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE,default=None,null=True)
    username = models.CharField(max_length=200, default=None,null=True)
    site_rank = models.IntegerField(default=None,null=True)
    site_rating = models.IntegerField(default=None,null=True)
    site_point = models.FloatField(default=None,null=True)
    site_ques_solved = models.IntegerField(default=None,null=True)
    site_repo = models.IntegerField(default=None,null=True)
    site_star = models.IntegerField(default=None,null=True)
    site_contribution = models.IntegerField(default=None,null=True)
    site_follower = models.IntegerField(default=None,null=True)
    site_following = models.IntegerField(default=None,null=True)
    is_active = models.BooleanField(default=False)
    no_of_sites = models.IntegerField(default=None,null=True)

    def __str__(self):
        return str(self.user) + " - " + str(self.site)
    
class GithubRank(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=None,null=True)
    language = models.CharField(max_length=200, default=None,null=True)
    city = models.CharField(max_length=200, default=None,null=True)
    city_rank = models.IntegerField(default=None,null=True)
    city_total = models.IntegerField(default=None,null=True)
    country = models.CharField(max_length=200, default=None,null=True)
    country_rank = models.IntegerField(default=None,null=True)
    country_total = models.IntegerField(default=None,null=True)
    world_rank = models.IntegerField(default=None,null=True)
    world_total = models.IntegerField(default=None,null=True)
    repos = models.IntegerField(default=None,null=True)
    stars = models.IntegerField(default=None,null=True)

    def __str__(self):
        return self.language
