from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from .company import NAMES, BRANCHES, not_nitw
from .forms import RegisterForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.


def home(request):
    responses = Experience.objects.all().order_by('-id')[:3]
    return render(request, 'home.html', {'responses': responses})


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        email = request.POST['email']
        print(email)
        if not_nitw(email):
            context = {
                'form': form,
                'alert': True,
                'message': "Please Use NITW MAIL"
            }
            # print(form.error_messages)
            return render(request, 'register.html', context=context)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return render(request, 'filter.html', {})
        else:
            context = {
                'form': form,
                'alert': True,
                'message': "Form is invalid <br>• Password shouldnt be common <br>• Password Should contain only letters and numbers"
            }
            # print(form.error_messages)
            return render(request, 'register.html', context=context)
    elif request.method == "GET":
        message = "Register"
        form = RegisterForm()
        context = {
            'form': form,
            'message': message
        }
        return render(request, 'register.html', context=context)


def company(request):
    if request.method == 'POST':
        filter = request.POST['filter']
        filter = filter.strip()
        print(filter)
        try:
            responses = Experience.objects.filter(
                cgpa_cutoff__lte=float(filter)).order_by('company', '-id')
            message = 'Companies You are eligible for with CGPA : ' + filter
        except:
            if filter.upper() in BRANCHES:
                responses = Experience.objects.filter(
                    branch__icontains=filter).order_by('-id')
                message = 'Interview Experience by branch ' + filter
            else:
                responses = Experience.objects.filter(
                    company__icontains=filter).order_by('-id')
                message = 'Interview Experience of ' + filter
            msg_empty = False
            if len(responses) == 0:
                msg_empty = 'OOPS! No responses for the query you are looking for.'
        return render(request, 'experience.html', {'responses': responses, 'message': message, 'msg_empty': msg_empty})
    elif request.method == 'GET':
        return render(request, 'filter.html', {'companies': NAMES})


def experience(request):
    responses = Experience.objects.order_by('company', '-id')
    message = 'All Interview Experiences'
    return render(request, 'experience.html', {'responses': responses, 'message': message})

# Pending Work


@login_required()
def write(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        batch = request.POST.get('batch')
        company = request.POST.get('company')
        cgpa = request.POST.get('cgpa')
        period = request.POST.get('period')
        branches = request.POST.getlist('branches')
        resume = request.POST.get('resume')
        aboutOT = request.POST.get('aboutOT')
        aboutOT1 = request.POST.get('aboutOT1')
        linktOT1 = request.POST.get('linkOT1')
        aboutOT2 = request.POST.get('aboutOT2')
        linktOT2 = request.POST.get('linkOT2')
        aboutOT3 = request.POST.get('aboutOT3')
        linktOT3 = request.POST.get('linkOT3')
        aboutOT4 = request.POST.get('aboutOT4')
        linktOT4 = request.POST.get('linkOT4')
        OTSummary = request.POST.get('OTSummary')
        interviewR1 = request.POST.get('interviewR1')
        interviewR2 = request.POST.get('interviewR2')
        interviewR3 = request.POST.get('interviewR3')
        suggestions = request.POST.get('suggestions')
        summary = aboutOT[:113]
        temp = Experience(
            user=User.objects.get(id=request.user.id),
            resume=resume,
            batch=batch,
            name=name,
            branch=' '.join(branches),
            cgpa_cutoff=cgpa,
            company=company,
            summary=summary,
            period=period,
            ot_summary=aboutOT,
            ot_question1=aboutOT1,
            ot_question1_link=linktOT1,
            ot_question2=aboutOT2,
            ot_question2_link=linktOT2,
            ot_question3=aboutOT3,
            ot_question3_link=linktOT3,
            ot_question4=aboutOT4,
            ot_question4_link=linktOT4,
            round1_details=interviewR1,
            round2_details=interviewR2,
            round3_details=interviewR3,
            final_summary=suggestions,
        )
        temp.save()
        user = request.user
        is_current_user = False
        if user.id == request.user.id:
            is_current_user = True
        posts = Experience.objects.filter(user=user)
        count = len(posts)
        context = {
            'user': user,
            'is_current_user': is_current_user,
            'posts': posts,
            'count': count
        }
        return render(request, 'profile.html', context)
    return render(request, 'write.html', {'message': False, 'companies': NAMES[:len(NAMES)-8]})


def about(request):
    return render(request, 'about.html', {})


def post(request, id):
    try:
        response = Experience.objects.get(pk=id)
        return render(request, 'post.html', {'response': response})
    except Experience.DoesNotExist:
        responses = Experience.objects.all().order_by('-id')[:3]
        return render(request, 'home.html', {'responses': responses})


@login_required()
def edit(request, id):
    post = Experience.objects.get(pk=id)
    if(post.user == request.user):
        if request.method == 'POST':
            post.name = request.POST.get('name')
            post.batch = request.POST.get('batch')
            post.company = request.POST.get('company')
            post.cgpa_cutoff = request.POST.get('cgpa')
            post.period = request.POST.get('period')
            post.branch = ' '.join(request.POST.getlist('branches'))
            post.resume = request.POST.get('resume')
            post.ot_summary = request.POST.get('aboutOT')
            post.ot_question1 = request.POST.get('aboutOT1')
            post.ot_question1_link = request.POST.get('linkOT1')
            post.ot_question2 = request.POST.get('aboutOT2')
            post.ot_question2_link = request.POST.get('linkOT2')
            post.ot_question3 = request.POST.get('aboutOT3')
            post.ot_question3_link = request.POST.get('linkOT3')
            post.ot_question4 = request.POST.get('aboutOT4')
            post.ot_question4_link = request.POST.get('linkOT4')
            post.round1_details = request.POST.get('interviewR1')
            post.round2_details = request.POST.get('interviewR2')
            post.round3_details = request.POST.get('interviewR3')
            post.final_summary = request.POST.get('suggestions')
            post.summary = post.ot_summary[:113]
            post.save()
            user = request.user
            is_current_user = False
            if user.id == request.user.id:
                is_current_user = True
            posts = Experience.objects.filter(user=user)
            count = len(posts)
            msg_empty = False
            if count == 0:
                msg_empty = 'No posts made by the user till now.'
            context = {
                'user': user,
                'is_current_user': is_current_user,
                'posts': posts,
                'count': count,
                'msg_empty': msg_empty
            }
            return render(request, 'profile.html', context)
        else:
            return render(request, 'write.html', {'message': "edit your current Experience", 'post': post, 'companies': NAMES[:len(NAMES)-8], 'update': True})
    else:
        responses = Experience.objects.all().order_by('-id')[:3]
        return render(request, 'home.html', {'responses': responses})


def delete(request, id):
    try:
        response = Experience.objects.get(pk=id)
        username = response.user.username
        response.delete()
        user = User.objects.get(username=username)
        is_current_user = False
        if user.id == request.user.id:
            is_current_user = True
        posts = Experience.objects.filter(user=user)
        count = len(posts)
        msg_empty = False
        if count == 0:
            msg_empty = 'No posts made by the user till now.'
        context = {
            'user': user,
            'is_current_user': is_current_user,
            'posts': posts,
            'count': count,
            'msg_empty': msg_empty
        }
        return render(request, 'profile.html', context)
    except Experience.DoesNotExist:
        responses = Experience.objects.all().order_by('-id')[:3]
        return render(request, 'home.html', {'responses': responses})


def profile(request, username):
    try:
        user = User.objects.get(username=username)
        is_current_user = False
        if user.id == request.user.id:
            is_current_user = True
        posts = Experience.objects.filter(user=user)
        count = len(posts)
        msg_empty = False
        if count == 0:
            msg_empty = 'No posts made by the user till now.'
        context = {
            'user': user,
            'is_current_user': is_current_user,
            'posts': posts,
            'count': count,
            'msg_empty': msg_empty,
        }
        return render(request, 'profile.html', context)
    except User.DoesNotExist:
        responses = Experience.objects.all().order_by('-id')[:3]
        return render(request, 'home.html', {'responses': responses})
