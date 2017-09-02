# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render,redirect,render_to_response
from django.shortcuts import get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from .models import Student, StudentSite, Site, GithubRank
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import UserForm,StudentForm, StudentSiteForm, ForgetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
import requests
from bs4 import BeautifulSoup
import string
import random

WorkingBaseURL = ' '

def RedirectSite(request):
    CurrentURL = get_current_site(request)
    RedirectURL = 'http://' + str(CurrentURL) + '/studentportal/'
    #print(RedirectURL)
    WorkingBaseURL = RedirectURL
    return redirect(RedirectURL)

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

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
    soup = BeautifulSoup(sauce.content,'html.parser')     # lxml is a parser
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

def githubRank(username):
    head = "http://git-awards.com/users/"
    var = username
    URL = head + var

    page  = requests.get(URL)
    soup = BeautifulSoup(page.content,'html.parser')
    a = list(soup.findAll('div',class_='col-md-3 info'))
    b = list(soup.findAll('td'))
    lang=[]
    f = 0
    for i in a:
        c = i.text.lstrip().rstrip()
        if 'your ranking' in c and f==0:
            f=1
            continue
        if 'ranking' in c:
            s=""
            d = c.split(" ")
            for j in d:
                if j!="ranking":
                    s+=j+" "
            lang.append(s.rstrip())

    #print(lang)
    record = []
    s=""
    k=0
    i=0
    while(i<len(b)):
        c = b[i].text.lstrip().rstrip()
        if "We couldn't find your city from your location on GitHub" in c:
            s = "0-0-"
            s+= "Worldwide-"

            d = b[i+2].text.split("/")
            r1=""
            r2=""
            for j in d[0]:
                if j>='0' and j<='9':
                    r1+=j
            for j in d[1]:
                if j>='0' and j<='9':
                    r2+=j
            s+= r1 + "-" + r2 + "-"
            s+= "Repos-"
            s+= b[i+4].text.lstrip().rstrip()+"-"
            s+= "Stars-"
            s+= b[i+6].text.lstrip().rstrip()
            s = lang[k] + "-" + s
            record.append(s)
            k+=1
            i = i+7
        else:
            s = b[i].text + "-"
            d = b[i+1].text.split("/")
            r1=""
            r2=""
            for j in d[0]:
                if j>='0' and j<='9':
                    r1+=j
            for j in d[1]:
                if j>='0' and j<='9':
                    r2+=j
            s+= r1 + "-" + r2 + "-"
            s += b[i+2].text + "-"
            d = b[i+3].text.split("/")
            r1=""
            r2=""
            for j in d[0]:
                if j>='0' and j<='9':
                    r1+=j
            for j in d[1]:
                if j>='0' and j<='9':
                    r2+=j
            s+= r1 + "-" + r2 + "-"
            i = i+3
            s+= "Worldwide-"

            d = b[i+2].text.split("/")
            r1=""
            r2=""
            for j in d[0]:
                if j>='0' and j<='9':
                    r1+=j
            for j in d[1]:
                if j>='0' and j<='9':
                    r2+=j
            s+= r1 + "-" + r2 + "-"
            s+= "Repos-"
            s+= b[i+4].text.lstrip().rstrip()+"-"
            s+= "Stars-"
            s+= b[i+6].text.lstrip().rstrip()
            s = lang[k] + "-" + s
            record.append(s)
            k+=1
            i = i+7

    return (record)


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

def codeforces(username):
    head = 'http://codeforces.com/profile/'
    var = username
    URL = head + var
    page = requests.get(URL)
    soup = BeautifulSoup(page.content,'html.parser')

    listRating = list(soup.findAll('div',class_="user-rank"))
    CheckRating = listRating[0].get_text()  #Check for rated or unrated
    if str(CheckRating) == '\nUnrated \n':
        # print('Not rated')
        out = 1000000
        return(out)
    else:
    # print('rated')
        listinfo = list((soup.find('div',class_="info")).findAll('li'))
        string = (listinfo[0].get_text())
        string = string.replace(" ","")
        str1,str2 = string.split('(')   # Well,.. don't judge me
        str3,str4 = str1.split(':')
        out = int((str4.strip()))
        print(out)
        return(out)

temp_object_list=[]

# def BaseView(request):
#     query = request.GET.get("q")
#     if query:
#        print('a')
#        temp_object_list = Student.object.filter(Q(enrollment_no__icontains=query)).order_by('enrollment_no')
#        return render(request,'student/base.html',{})

#class IndexView(generic.ListView):
#    template_name = 'student/index.html'
#    def get_queryset(self):
#        #query = request.GET.get("q")
#        object_list =  Student.objects.filter().order_by('enrollment_no')
#        query = self.request.GET.get("q")
#        if query:
#           #print('a')
#           temp_object_list = object_list.filter(Q(enrollment_no__icontains=query)).order_by('enrollment_no')
#           object_list = temp_object_list
#        return object_list

class IndexView(View):
    template_name = 'student/index.html'
    def get(self,request):
        #query = request.GET.get("q")
        sem1 =  Student.objects.filter(current_semester=1).order_by('enrollment_no')
        sem2 =  Student.objects.filter(current_semester=2).order_by('enrollment_no')
        sem3 =  Student.objects.filter(current_semester=3).order_by('enrollment_no')
        sem4 =  Student.objects.filter(current_semester=4).order_by('enrollment_no')
        sem5 =  Student.objects.filter(current_semester=5).order_by('enrollment_no')
        sem6 =  Student.objects.filter(current_semester=6).order_by('enrollment_no')
        sem7 =  Student.objects.filter(current_semester=7).order_by('enrollment_no')
        sem8 =  Student.objects.filter(current_semester=8).order_by('enrollment_no')
        sem9 =  Student.objects.filter(current_semester=9).order_by('enrollment_no')
        sem10 =  Student.objects.filter(current_semester=10).order_by('enrollment_no')

        object_list = []
        query = self.request.GET.get("q")
        if query:
           #print('a')
           temp_object_list = Student.objects.filter(Q(user__first_name__contains=query) | Q(enrollment_no__icontains=query)).order_by('enrollment_no')
           object_list = temp_object_list

        context = {'object_list':object_list,'sem1':sem1,'sem2':sem2,'sem3':sem3,'sem4':sem4,'sem5':sem5,'sem6':sem6,'sem7':sem7,'sem8':sem8,'sem9':sem9,'sem10':sem10}
        return render(request,'student/index.html',context)

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
            password = id_generator()
            user.set_password(password)
            user.save()

            #send_mail(subject, message, from_email, to_list, fail_silently=True)
            subject = 'Thankyou for registering'
            message = 'Welcome to IIITA profilePortal. Your username = ' + str(username) + ' Your password = ' + password
            from_email = settings.EMAIL_HOST_USER
            to_list = [user.email,settings.EMAIL_HOST_USER]
            send_mail(subject,message,from_email,to_list,fail_silently=True)

            return render(request,self.template_name,{ 'passwordSent':'Password successfully sent to your email','form': form})

        return render(request, self.template_name, {'form': form})

class UserPasswordChange(View):

    template_name = 'student/password_form.html'

    def get(self, request):
        if request.user.is_authenticated():
            form = PasswordChangeForm(request.user)
            return render(request, self.template_name, {'form': form})
        else:
            return redirect('student:login')

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('student:index')
        else:
            messages.error(request, 'Please correct the error below.')


        return render(request, self.template_name, {'form': form})

class ForgetPassword(View):

    template_name = 'student/forget_password_form.html'

    def get(self, request):
        if request.user.is_authenticated():
            return redirect('student:index')
        else:
            form = ForgetPasswordForm(request.GET)
            return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ForgetPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']

            usercount = User.objects.filter(username=username).count()
            if usercount==1:
                user = User.objects.get(username=username)
                if user.email==email:
                    password = id_generator()
                    user.set_password(password)
                    user.save()

                    #send_mail(subject, message, from_email, to_list, fail_silently=True)
                    subject = 'Password change'
                    message = 'You forgot your passwordso we are sending new password. Change this password once you log in. Your username = ' + username + ' Your new password = ' + password
                    from_email = settings.EMAIL_HOST_USER
                    to_list = [user.email,settings.EMAIL_HOST_USER]
                    send_mail(subject,message,from_email,to_list,fail_silently=True)

                    messages.success(request, 'Your password was successfully sent!')
                    return redirect('student:index')
                else:
                    return render(request, self.template_name, {'form': form})
            else:
                messages.error(request, 'no such user exist')
                return render(request, self.template_name, {'form': form})

        else:
            messages.error(request, 'Please correct the error below.')


        return render(request, self.template_name, {'form': form})

class StudentCreate(CreateView):
    model = Student
    fields = '__all__'
    success_url = reverse_lazy('student:index')

class StudentFormView(View):

    form_class = StudentForm
    template_name = 'student/studentcreate.html'

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
    template_name = 'student/studentupdate.html'

    def get(self, request):
        if request.user.is_authenticated():
            my_record = Student.objects.filter(id=request.user.id)
            if my_record.count()!=0:
                my_record = Student.objects.get(id=request.user.id)
                form = self.form_class(instance=my_record)
                return render(request, self.template_name, {'form': form})
            else:
                return redirect('student:studentcreate')
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
                if record.site.site_name == 'codeforces':
                    out = codeforces(record.username)
                    record.site_rating = out
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
    template_name = 'student/addsite.html'

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
                if site1 == 'codeforces':
                    out = codeforces(form.cleaned_data['username'])
                    print(out)
                    studentsite.site_rating = out

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

class GithubRankView(View):

    def get(self,request):
        my_site=Site.objects.filter(site_name="github")
        my_record = StudentSite.objects.filter(user=request.user)
        for j in my_record:
            if j.site.site_name=="github":
                github = githubRank(j.username)
                for i in github:
                    record = i.split("-")
                    my_lang = GithubRank.objects.filter(user=request.user).filter(language=record[0])
                    if my_lang:
                        my_lang = GithubRank.objects.filter(user=request.user).filter(language=record[0]).get(user=request.user)
                        if record[1]=="0":
                            #instance = GithubRank(user=request.user,language=record[0],world_rank=int(record[4]),world_total=int(record[5]),repos=int(record[7]),stars=int(record[9]))
                            my_lang.world_rank = int(record[4])
                            my_lang.world_total = int(record[5])
                            my_lang.repos = int(record[7])
                            my_lang.stars = int(record[9])
                            my_lang.save()
                        else:
                            #instance = GithubRank(user=request.user,language=record[0],city=record[1],city_rank=int(record[2]),city_total=int(record[3]),country=record[4],country_rank=int(record[5]),country_total=int(record[6]),world_rank=int(record[8]),world_total=int(record[9]),repos=int(record[11]),stars=int(record[13]))
                            my_lang.city_rank = int(record[2])
                            my_lang.city_total = int(record[3])
                            my_lang.country_rank = int(record[5])
                            my_lang.country_total = int(record[6])
                            my_lang.world_rank = int(record[8])
                            my_lang.world_total = int(record[9])
                            my_lang.repos = int(record[11])
                            my_lang.stars = int(record[13])
                            my_lang.save()
                    else:

                        if record[1]=='0':

                            instance = GithubRank(user=request.user,language=record[0],world_rank=int(record[4]),world_total=int(record[5]),repos=int(record[7]),stars=int(record[9]))
                            instance.save()
                        else:
                            print(record[13])
                            instance = GithubRank(user=request.user,language=record[0],city=record[1],city_rank=int(record[2]),city_total=int(record[3]),country=record[4],country_rank=int(record[5]),country_total=int(record[6]),world_rank=int(record[8]),world_total=int(record[9]),repos=int(record[11]),stars=int(record[13]))
                            instance.save()
        CurrentURL = get_current_site(request)
        RedirectURL = 'http://' + str(CurrentURL) + '/studentportal/' + str(request.user.id)+"/"

        s = RedirectURL
        return redirect(s)


class RanksView(View):

    def get(self,request):
        codechef = StudentSite.objects.filter().order_by('-site_rating')
        spoj = StudentSite.objects.filter().order_by('-site_point')
        github = StudentSite.objects.filter().order_by('-site_contribution')
        codebuddy = StudentSite.objects.filter().order_by('-site_point')
        codeforces = StudentSite.objects.filter().order_by('-site_rating')
        javascript = GithubRank.objects.filter(language="javascript").order_by('world_rank')
        c = GithubRank.objects.filter(language="c").order_by('world_rank')
        cpp = GithubRank.objects.filter(language="c++").order_by('world_rank')
        php = GithubRank.objects.filter(language="php").order_by('world_rank')
        python = GithubRank.objects.filter(language="python").order_by('world_rank')
        html = GithubRank.objects.filter(language="html").order_by('world_rank')
        css = GithubRank.objects.filter(language="css").order_by('world_rank')
        processing = GithubRank.objects.filter(language="processing").order_by('world_rank')
        ruby = GithubRank.objects.filter(language="ruby").order_by('world_rank')

        context = {'codechef':codechef, 'spoj':spoj, 'github':github,'codebuddy':codebuddy,'codeforces':codeforces,'javascript':javascript,'c':c,'cpp':cpp,'php':php,'python':python,'html':html,'css':css,'processing':processing,'ruby':ruby}
        return render(request,'student/ranks.html',context)


def logout_view(request):
    logout(request)
    return redirect('student:index')
