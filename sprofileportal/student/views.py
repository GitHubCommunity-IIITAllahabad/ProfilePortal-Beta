# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from .models import Student, StudentSite
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import UserForm,StudentForm, StudentSiteForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
import requests
from bs4 import BeautifulSoup

def codechef(username):
    head = "https://wwww.codechef.com/users/"
    URL = head + username

    page  = requests.get(URL)
    soup = BeautifulSoup(page.content,'html.parser')

    #These three lines give the Rating of the user.
    listRating = list(soup.findAll('div',class_="rating-number"))
    rating = list(listRating[0].children)
    rating = rating[0]
    out = str(rating)
    #print ("Rating: "+rating)

    listGCR = []  #Global and country ranking.
    listRanking = list(soup.findAll('div',class_="rating-ranks"))
    rankingSoup = listRanking[0] 
    for item in rankingSoup.findAll('a'):
            listGCR.append(item.get_text()) #Extracting the text from all anchor tags
    #print ("Global Ranking: "+listGCR[0])
    #print ("Country Ranking: "+listGCR[1])
    out = out + " " + str(listGCR[0])
    return out

def spoj(username):
    base = "https://spoj.com/users/"
    var = username
    url = base + var
    sauce = requests.get(url) 
    soup = BeautifulSoup(sauce.content,'lxml')     # lxml is a parser
    #print(soup.prettify())
    iList = []
    info = (soup.find_all('p'))
    for i in info:
        iList.append(i.text)

    #print (iList[2]) #World rank
    #print (iList[3]) #Institution
    no_of_questions = int(soup.find('dd').text)
    #print(" no. of questions = ",no_of_questions)
    s = str(iList[2].lstrip())+" "+str(no_of_questions)
    return s

def github(username):
    url = "https://github.com/"+username
    sauce = requests.get(url)   
    soup = BeautifulSoup(sauce.content,'html.parser')     # lxml is a parser
    #print(soup)

    things = soup.find_all('span',class_='Counter')
    repoNo = int(things[0].text)
    starsNo = int(things[1].text)
    FollowersNo = int(things[2].text)
    FollowingNo = int(things[3].text)

    contribution = (soup.find('h2',class_='f4 text-normal mb-2').text).lstrip().split(" ")
    no_contribution = int(contribution[0])
    #print (no_contribution)
    s = str(repoNo)+" "+str(starsNo)+" "+str(FollowersNo)+" "+str(FollowingNo)+" "+str(no_contribution)
    return (s)

def codebuddy(username):
    URL = "https://codebuddy.co.in/ranks/practice"
    page  = requests.get(URL)
    soup = BeautifulSoup(page.content,'html.parser')
    table = list(soup.find_all('tr'))
    for i in table:
        parameters = list(i.find_all('label'))
        #print (i.find('label',class_="highlight").text)
        if str(parameters[1].text)==username:
            output = str(int(parameters[0].text))+" "+str(int(parameters[2].text))+" "+str(float(parameters[3].text))
            return (output)
    return (-1)

class IndexView(generic.ListView):
    template_name = 'student/index.html'

    def get_queryset(self):
        return Student.objects.filter().order_by('enrollment_no')

class DetailView(generic.DetailView):
    model = Student
    template_name = 'student/detail.html'

class AlbumCreate(CreateView):
    model = Student
    

class StudentUpdate(UpdateView):
    model = Student
    fields = ['first_name','last_name','current_semester','graduation_year']
    success_url = reverse_lazy('student:index')

class UserFormView(View):
    form_class = UserForm
    template_name = 'student/registration_form.html'

    #display a blank form
    def get(self, request):
        if not request.user.is_authenticated():
            form = self.form_class(None)
            return render(request, self.template_name, {'form': form})
        else:
            return redirect('student:index')
    #process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            #cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # returns User object if credentials are correct
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('http://127.0.0.1:8000/studentportal/register/studentcreate/')

        return render(request, self.template_name, {'form': form})

class StudentCreate(CreateView):
    model = Student
    fields = '__all__'
    success_url = reverse_lazy('student:index')

class StudentFormView(View):
    
    form_class = StudentForm
    template_name = 'student/registration_form.html'
        
    def get(self, request):
        if request.user.is_authenticated():
            my_record = Student.objects.filter(id=request.user.id).count()
            if my_record!=0:
                return redirect('student:index')
            else:
                form = self.form_class(None)
                return render(request, self.template_name, {'form': form})
        else:
            return redirect('student:index')

    def post(self, request):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            count = Student.objects.filter(user=request.user).count()
            if count==0:
                student = form.save(commit=False)
                student.user = request.user
                student.is_active = True
                student.id = request.user.id
                student.save()
                return redirect('student:index')
            else:
                return render(request, self.template_name, {'form': form})

        return render(request, self.template_name, {'form': form})

class UpdateStudentFormView(View):
    
    form_class = StudentForm
    template_name = 'student/registration_form.html'
        
    def get(self, request):
        if request.user.is_authenticated():
            my_record = Student.objects.get(id=request.user.id)
            form = self.form_class(instance=my_record)
            return render(request, self.template_name, {'form': form})
        else:
            return redirect('student:index')

    def post(self, request):
        my_record = Student.objects.get(id=request.user.id)
        form = self.form_class(request.POST,instance=my_record)
        
        if form.is_valid():
            student = form
            student.save()
            return redirect('student:index')
        else:
            return render(request, self.template_name, {'form': form})

        return render(request, self.template_name, {'form': form})

class StudentSiteFormView(View):
    
    form_class = StudentSiteForm
    template_name = 'student/registration_form.html'
        
    def get(self, request):
        if request.user.is_authenticated():
            form = self.form_class(None)
            return render(request, self.template_name, {'form': form})
        else:
            return redirect('student:index')

    def post(self, request):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            studentsite = form.save(commit=False)
            studentsite.user = request.user
            studentsite.is_active = True
            site1 = str(form.cleaned_data.get('site'))
            if site1 == 'codechef':
                out = codechef(form.cleaned_data['username']).split(" ")
                studentsite.site_rating = int(out[0])
                studentsite.site_rank = int(out[1])
            if site1 == 'spoj':
                out = spoj(form.cleaned_data['username']).split(" ")
                studentsite.site_rank = int(out[2].lstrip('#'))
                studentsite.site_point = float(out[3].lstrip('('))
                studentsite.site_ques_solved = int(out[5])
            if site1 == 'github':
                out = github(form.cleaned_data['username']).split(" ")
                studentsite.site_repo = int(out[0])
                studentsite.site_star = int(out[1])
                studentsite.site_follower = int(out[2])
                studentsite.site_following = int(out[3])
                studentsite.site_contribution = int(out[4])
            if site1 == 'codebuddy':
                out = codebuddy(form.cleaned_data['username']).split(" ")
                studentsite.site_rank = int(out[0])
                studentsite.site_ques_solved = int(out[1])
                studentsite.site_point = float(out[2])
                
            studentsite.save()
            s = "http://127.0.0.1:8000/studentportal/"+str(request.user.id)+"/"
            return redirect(s)
        else:
            return render(request, self.template_name, {'form': form})

        return render(request, self.template_name, {'form': form})

class RanksView(View):

    def get(self,request):
        codechef = StudentSite.objects.filter().order_by('site_rating')
        spoj = StudentSite.objects.filter().order_by('site_point')
        github = StudentSite.objects.filter().order_by('site_contribution')
        codebuddy = StudentSite.objects.filter().order_by('site_point')
        context = {'codechef':codechef, 'spoj':spoj, 'github':github,'codebuddy':codebuddy}
        return render(request,'student/ranks.html',context)
        

def logout_view(request):
    logout(request)
    return redirect('student:index')
