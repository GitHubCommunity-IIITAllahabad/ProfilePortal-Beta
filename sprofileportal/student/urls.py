"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from django.contrib.auth import views as auth_views
from . import views

app_name = 'student'

urlpatterns = [
    # /music/
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^login/$', auth_views.login, {'template_name': 'student/login.html'}, name='login'),
     url(r'^logout/$', views.logout_view, name='logout'),
     url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^ranks/$', views.RanksView.as_view(), name='ranks'),
     #url(r'^studentcreate/$', views.StudentCreate.as_view(), name='studentcreate'),
     url(r'^register/studentcreate/$', views.StudentFormView.as_view(), name='studentcreate'),
    url(r'^register/studentupdate/$', views.UpdateStudentFormView.as_view(), name='studentupdate'),
    url(r'^register/studentsite/$', views.StudentSiteFormView.as_view(), name='studentsite'),
    # /music/<album_id>/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    
    url(r'album/add/$', views.AlbumCreate.as_view(), name='album-add'),
    
    #url(r'^student/(?P<pk>[0-9]+)/$', views.StudentUpdate.as_view(), name='album-update'),
    
]
