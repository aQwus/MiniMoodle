from django.shortcuts import render , get_object_or_404 , redirect ,render_to_response
from django.http import HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.views import generic
from django.views.generic import View
from django.contrib.auth import authenticate, login as auth_login , logout as auth_logout
from django.contrib import auth
from django.template.defaulttags import csrf_token
from django.contrib.auth.forms import UserCreationForm
from .models import Account , Teacher ,Student, Course, StudCourse, Message
import datetime
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.

def login(request):
    if request.user:
        logout(request)
    return render(request , 'course/login.html',{});

def loggedin(request):

    u = Account.objects.filter(user = request.user)
    if u[0].is_teach == True:
        t = Teacher.objects.filter(user = request.user)
        if not t:
            print("hi")
            p = Teacher()
            p.user = request.user
            p.save()
            type = "teacher"
        else:
            p = t[0]
        myc = Course.objects.filter(teacher = p)
        return render(request, 'course/teacher.html',{"user" : request.user, "mycourses": myc})
    else:
        t = Student.objects.filter(user=request.user)
        if not t:
            print("hi")
            p = Student()
            p.user = request.user
            p.save()
        else:
            p = t[0]
        s = Student.objects.filter(user = request.user)

        myc = StudCourse.objects.filter(stud = s[0])
        type = "stud"
        return render(request,'course/student.html',{"student": request.user ,"mycourses":myc,"courses": Course.objects.filter()})


def auth(request):
    u = request.POST.get('username', ' ')
    p = request.POST.get('password', ' ')
    user = authenticate(username=u, password=p)
    if user is not None:
        auth_login(request, user)
        return HttpResponseRedirect('/loggedin')
    else:
        messages.add_message(request, messages.SUCCESS, 'Unable to login either User name or password is incorrect!!')
        return HttpResponseRedirect('/')

def addct(request):
    n = request.POST.get('name','')
    i = request.POST.get('info','')

    if n == '' or i == '':
        print("yoyo")
        return HttpResponseRedirect("/loggedin")
    else:
        p = Course.objects.filter(name = 'n')
        if p:
            return HttpResponseRedirect("/loggedin")
        else:
            t = Course()
            t.name = n
            t.Inf = i
            k = Teacher.objects.filter(user = request.user)
            t.teacher = k[0]
            try:
                t.save()
            except:
                messages.add_message(request, messages.SUCCESS,
                                     'Course Exists!!')
            return HttpResponseRedirect("/loggedin")

def selectprof(request):
    if request.method == 'GET':
        course = request.GET.get('course')
        print(course)
        c = Course.objects.filter(name = course)
        print(c[0].Inf)
        s = Student.objects.filter(user = request.user)
        d = StudCourse.objects.filter(course = c[0] , stud = s[0])
        try:
            a = d[0]
            return render(request,'course/coursedetails.html',{"course": c[0],"a":a,"student":request.user})
        except:
            return render(request,'course/coursedetails.html',{"course": c[0],"a":"","student":request.user})




def addcs(request):
    coursen = request.GET.get('course')
    course = Course.objects.filter(name = coursen)
    user1 = request.user
    stud1 = Student.objects.filter(user = user1)[0]
    print(stud1)
    print(course)
    a = StudCourse()
    a.stud = stud1
    a.course = course[0]
    a.date = datetime.date.today()
    a.time = datetime.datetime.now().time()
    a.save()
    return HttpResponseRedirect("/loggedin")

def removesc(request):
    coursen = request.GET.get('course')
    course = Course.objects.filter(name = coursen)
    s = Student.objects.filter(user=request.user)

    cs = StudCourse.objects.filter(course = course[0],stud = s[0])
    cs[0].delete()
    return HttpResponseRedirect("/loggedin")

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')

def deletetc(request):
    coursed = request.GET.get('course')
    c = Course.objects.filter(name = coursed)
    c.delete()
    return HttpResponseRedirect("/loggedin")

def addmessage(request):
    print(datetime.datetime.now().time())
    print(datetime.date.today())
    course = request.GET.get('course')
    if request.method == 'POST':
        a = Message()
        a.course = Course.objects.filter(name= request.POST.get('course'))[0]
        a.subject = request.POST.get('title')
        a.msg = request.POST.get('message')
        a.date = datetime.date.today()
        a.time = datetime.datetime.now().time()
        a.save()
        return HttpResponseRedirect("/loggedin")
    else:
        messagesc = Message.objects.filter(course = Course.objects.filter(name = course)[0])
        return render(request,'course/addmessage.html',{"course": course,"messagesc": messagesc})

def studentmessage(request):
    scs = StudCourse.objects.filter(stud=Student.objects.filter(user=request.user)[0])
    coursess = []
    for scc in scs:
        c = {"course": scc.course,"message":""}
        messagesd = Message.objects.filter(course = scc.course)
        d = []
        for messag in messagesd:
            if messag.date > scc.date or (messag.date == scc.date and messag.time > scc.time):
                d.append(messag)

        c["message"] = d
        coursess.append(c)

    return render(request,'course/studentmsg.html',{"courses":coursess,"student":request.user})