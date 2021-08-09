from django.http.response import HttpResponse
from django.shortcuts import render
from .models import *
from .company import NAMES, BRANCHES, not_nitw
from .forms import RegisterForm
from django.shortcuts import  render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    responses = Experience.objects.all().order_by('-id')[:3]
    return render(request, 'home.html',{'responses':responses})

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        email = request.POST['email']
        print(email)
        if not_nitw(email):
            context = {
            'form':form,
            'alert' : True,
            'message' : "Please Use NITW MAIL"
            }
            # print(form.error_messages)
            return render(request, 'register.html',context=context)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return render(request, 'filter.html',{})
        else:
            context = {
            'form' : form,
            'alert' : True,
            'message' : "Form is invalid <br>• Password shouldnt be common <br>• Password Should contain only letters and numbers"
            }
            # print(form.error_messages)
            return render(request, 'register.html',context=context)
    elif request.method == "GET":
        message = "Good Morning"
        form = RegisterForm()
        context = {
        'form' : form,
        'message' : message
        }
        return render(request, 'register.html',context=context)

def company(request):
    if request.method == 'POST':
        filter = request.POST['filter']
        filter  = filter.strip()
        print(filter)
        try:
            responses = Experience.objects.filter(cgpa_cutoff__lte = float(filter)).order_by('company','-id')
            message = 'Companies You are eligible for with CGPA : ' + filter
        except:
            if filter.upper() in BRANCHES:
                responses = Experience.objects.filter(branch__icontains=filter).order_by('-id')
                message = 'Interview Experience by branch ' + filter
            else:
                responses = Experience.objects.filter(company__icontains=filter).order_by('-id')
                message = 'Interview Experience of ' + filter
        return render(request, 'experience.html',{'responses':responses,'message':message})
    elif request.method == 'GET':
        return render(request, 'filter.html',{'companies':NAMES})

def experience(request):
    responses = Experience.objects.order_by('company','-id')
    message = 'All Interview Experiences'
    return render(request, 'experience.html',{'responses':responses,'message':message})

# Pending Work
@login_required()
def write(request):
    id = request.user.id
    print(id)
    first_name = request.user
    print(first_name)
    if request.method == 'POST':
        lop = request.POST.getlist('branches')
        return render(request, 'write.html', {})
    return render(request, 'write.html', {})


def about(request):
    return render(request, 'about.html', {})