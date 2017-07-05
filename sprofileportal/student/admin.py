# -*- coding: utf-8 -*-
#admin username: softdev
#admin password: softdev123
from __future__ import unicode_literals

from django.contrib import admin
from .models import Student, Site, StudentSite, GithubRank

admin.site.register(Student)
admin.site.register(Site)
admin.site.register(StudentSite)
admin.site.register(GithubRank)

