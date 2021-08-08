from django.http.response import HttpResponse
from django.shortcuts import render
from .models import *
from .company import NAMES

# Create your views here.
def home(request):
    responses = Experience.objects.all().order_by('-id')[:3]
    return render(request, 'home.html',{'responses':responses})

def login(request):
    return render(request, 'login.html',{})

def register(request):
    return render(request, 'register.html',{})

def company(request):
    if request.method == 'POST':
        company_name = request.POST['company']
        responses = Experience.objects.filter(company__icontains=company_name)
        message = 'Interview Experience of ' + company_name
        return render(request, 'experience.html',{'responses':responses,'message':message})
    elif request.method == 'GET':
        return render(request, 'filter.html',{'companies':NAMES})

def experience(request):
    responses = Experience.objects.order_by('company','-id')
    message = 'All Interview Experiences'
    return render(request, 'experience.html',{'responses':responses,'message':message})


def write(request):
    return render(request, 'write.html', {})


def about(request):
    return render(request, 'about.html', {})