# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect,render_to_response
from django.shortcuts import get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from .models import Student, StudentSite, Site
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import UserForm,StudentForm, StudentSiteForm
from django.contrib.auth import logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
import requests
from bs4 import BeautifulSoup

WorkingBaseURL = ' '

def RedirectSite(request):
    CurrentURL = get_current_site(request)
    RedirectURL = 'http://' + str(CurrentURL) + '/studentportal/'
    #print(RedirectURL)
    WorkingBaseURL = RedirectURL
    return redirect(RedirectURL)

def codechef(username):
    head = "https://wwww.codechef.com/users/"
    URL = head + username

    page  = requests.get(URL)
    soup = BeautifulSoup(page.content,'html.parser')

    #These three lines give the Rating of the user.
    listRating = list(soup.findAll('div',class_="rating-number"))
    rating = list(listRating[0].children)
    rating = rating[0]
    out = str(rating.replace(',',''))
    #print ("Rating: "+rating)

    listGCR = []  #Global and country ranking.
    listRanking = list(soup.findAll('div',class_="rating-ranks"))
    rankingSoup = listRanking[0] 
    for item in rankingSoup.findAll('a'):
            listGCR.append(item.get_text()) #Extracting the text from all anchor tags
    #print ("Global Ranking: "+listGCR[0])
    #print ("Country Ranking: "+listGCR[1])
    out = out + " " + str(listGCR[0].replace(',',''))
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
    no_of_questions = int((soup.find('dd').text).replace(',',''))
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
    contribution_no = int(contribution[0].replace(',',''))
    #print (contribution_no)
    s = str(repoNo)+" "+str(starsNo)+" "+str(FollowersNo)+" "+str(FollowingNo)+" "+str(contribution_no)
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
            output = str(int((parameters[0].text).replace(',','')))+" "+str(int((parameters[2].text).replace(',','')))+" "+str(float(parameters[3].text))
            return (output)
    return (-1)

temp_object_list=[]

# def BaseView(request):
#     query = request.GET.get("q")
#     if query:
#        print('a') 
#        temp_object_list = Student.object.filter(Q(enrollment_no__icontains=query)).order_by('enrollment_no')
#        return render(request,'student/base.html',{})

class IndexView(generic.ListView):
    template_name = 'student/index.html'
    def get_queryset(self):
        #query = request.GET.get("q")
        object_list =  Student.objects.filter().order_by('enrollment_no')
        query = self.request.GET.get("q")
        if query:
           #print('a') 
           temp_object_list = object_list.filter(Q(enrollment_no__icontains=query)).order_by('enrollment_no')
           object_list = temp_object_list
        return object_list

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

class UpdateStudentSiteFormView(View):
    def get(self, request):
        if request.user.is_authenticated():
            my_record = StudentSite.objects.filter(user=request.user)
            # print(my_record)
            for record in my_record:
                
                if record.site.site_name == 'codechef':
                    out = codechef(record.username).split(" ")
                    record.site_rating = int(out[0])
                    record.site_rank = int(out[1])
                    record.save()
                if record.site.site_name == "github":
                    out = github(record.username).split(" ")
                    record.site_repo = int(out[0])
                    record.site_star = int(out[1])
                    record.site_follower = int(out[2])
                    record.site_following = int(out[3])
                    record.site_contribution = int(out[4])
                    record.save()

                if record.site.site_name == 'spoj':
                    out = spoj(record.username).split(" ")
                    record.site_rank = int(out[2].lstrip('#'))
                    record.site_point = float(out[3].lstrip('('))
                    record.site_ques_solved = int(out[5])
                    record.save()
                if record.site.site_name == 'codebuddy':
                    out = codebuddy(record.username).split(" ")
                    record.site_rank = int(out[0])
                    record.site_ques_solved = int(out[1])
                    record.site_point = float(out[2])
                    record.save()
            # s = "http://127.0.0.1:8000/studentportal/"+str(request.user.id)+"/"
            CurrentURL = get_current_site(request)
            RedirectURL = 'http://' + str(CurrentURL) + '/studentportal/' + str(request.user.id) + "/"
            # print(s)
            # print(CurrentURL)
            return redirect(RedirectURL)
        else:
            return redirect('student:index')
    
    
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
            my_record = StudentSite.objects.filter(user=request.user)
            flag=0
            for record in my_record:
                if record.site.site_name == str(form.cleaned_data.get('site').site_name):
                    flag=1
            my_record = StudentSite.objects.filter()
            for record in my_record:
                if record.site.site_name == str(form.cleaned_data.get('site').site_name) and record.username.lower() == str(form.cleaned_data.get('username').lower()):
                    flag=1
                
            if flag==0:
                studentsite = form.save(commit=False)
                studentsite.user = request.user
                studentsite.is_active = True
                site1 = str(form.cleaned_data.get('site').site_name)
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
                # s = "http://127.0.0.1:8000/studentportal/"+str(request.user.id)+"/"
                CurrentURL = get_current_site(request)
                RedirectURL = 'http://' + str(CurrentURL) + '/studentportal/' + str(request.user.id) + "/"
                return redirect(RedirectURL)
            else:
                # s = "http://127.0.0.1:8000/studentportal/"+str(request.user.id)+"/"
                return render(request,self.template_name,{'message': 'Username for for the site Already added','form':form})

        else:
            return render(request, self.template_name, {'form': form})

        return render(request, self.template_name, {'form': form})

class RanksView(View):

    def get(self,request):
        codechef = StudentSite.objects.filter().order_by('-site_rating')
        spoj = StudentSite.objects.filter().order_by('-site_point')
        github = StudentSite.objects.filter().order_by('-site_contribution')
        codebuddy = StudentSite.objects.filter().order_by('-site_point')
        context = {'codechef':codechef, 'spoj':spoj, 'github':github,'codebuddy':codebuddy}
        return render(request,'student/ranks.html',context)
        

def logout_view(request):
    logout(request)
    return redirect('student:index')
