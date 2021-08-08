from django.http.response import HttpResponse
from django.shortcuts import render
from .models import *
from .company import NAMES, BRANCHES

# Create your views here.
def home(request):
    responses = Experience.objects.all().order_by('-id')[:3]
    return render(request, 'home.html',{'responses':responses})

def register(request):
    return render(request, 'register.html',{})

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


def write(request):
    if request.method == 'POST':
        lop = request.POST.getlist('branches')
        print(lop)
        return render(request, 'write.html', {})
    return render(request, 'write.html', {})


def about(request):
    return render(request, 'about.html', {})