from django.http.response import HttpResponse
from django.shortcuts import render, redirect,HttpResponseRedirect
from .models import *
from .company import *
from .forms import RegisterForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login,update_session_auth_hash,authenticate
from django.contrib.auth.forms import PasswordChangeForm,PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic import TemplateView,CreateView,DeleteView,ListView,DetailView,UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse,reverse_lazy
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
# Create your views here.
import random
from django.core.mail import send_mail
@login_required()
def home(request):
    # if not request.user.is_staff:
    #     return HttpResponseRedirect(reverse('write'))
    responses = Experience.objects.all().order_by('-id')[:3]
    return render(request, 'home.html', {'responses': responses})
def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'internito.pythonanywhere.com',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'https',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'internito123@gmail.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})

def signin(request):
    context={"msg":""}
    if request.method == "POST":
        user=User.objects.filter(username=request.POST.get("username")).count()
        if user:
            user=User.objects.get(username=request.POST.get("username"))
            ev=Emailverify.objects.filter(user=user).count()
            user=authenticate(username=request.POST.get("username"),password=request.POST.get("password"))
            if ev==1 and user is not None:
                ev=Emailverify.objects.get(user=user)
                print(ev.status)
                if ev.status or user.is_staff:
                    print("hello")
                    login(request,user)
                    return HttpResponseRedirect(reverse('home'))
            elif ev==1:
                context["msg"]="Username or Password Wrong"
                return render(request,'login.html',context)
            elif ev>1:
                ev=Emailverify.objects.filter(user=user).delete()
            sendcode(user,user.email)
            return HttpResponseRedirect(reverse('verifycode',kwargs={'user':user}))
        else:
            context["msg"]="NO USER FOUND!!"
            return render(request,'login.html',context)
    else:
        return render(request,'login.html',context)

def sendcode(user,email):
    code=random.randrange(100000,999999)
    ad=Emailverify.objects.create(user=user,code=code,status=False)
    ad.save()
    print(email)
    send_mail(
         'Welcome to interNito',
         'Confirm your email by Verification code {} ,you are receiving this email as you want email verfication with us'.format(ad.code),
         'internito123@gmail.com',
         [email],
         fail_silently=False)

def verifycode(request,user):

    context={"msg":""}
    if request.method == "POST":
        code=request.POST.get("code")
        ev=Emailverify.objects.get(user=User.objects.get(username=user))
        if int(code) == int(ev.code) :
            ev.status="True"
            ev.save()
            print(ev.status)
            return HttpResponseRedirect(reverse(signin))
        else:
            context["msg"]="Wrong Code Entered"
    return render(request,"verifycode.html",context)

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        email = request.POST['email']
        print(email)
        if not_nitw(email):
            context={"msg":"Please Enter Student Mail!!!"}
            return render(request, 'register.html', context=context)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect(reverse(signin))
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
def feedback(request):
    if request.method == "POST":
        text=request.POST.get('feedback')
        print(text)
        send_mail(
            'FeedBack',
             '''Hey admin!! We recieved a feedback response from {}
{}'''.format(request.user.username,text),
             'internito123@gmail.com',
             ADMIN_EMAILS,
             fail_silently=False)
        return HttpResponseRedirect(reverse('feedback_reveive'))
    else:
        return render(request,'feedback.html')
class FeedbackReceive(TemplateView):
    template_name='tq.html'
@login_required()
def company(request):
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('write'))
    msg_empty= False
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

@login_required()
def experience(request):
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('write'))
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
        return HttpResponseRedirect(reverse('profile',kwargs={'username':request.user.username}))
    return render(request, 'write.html', {'message': False, 'companies': NAMES[:len(NAMES)-8]})

@login_required()
def about(request):
    return render(request, 'about.html', {})

@login_required()
def post(request, id):
    try:
        response = Experience.objects.get(pk=id)
        return render(request, 'post.html', {'response': response})
    except Experience.DoesNotExist:
        return HttpResponseRedirect(reverse('home'))


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
            return HttpResponseRedirect(reverse('profile',kwargs={'username':request.user.username}))
        else:
            return render(request, 'write.html', {'message': "edit your current Experience", 'post': post, 'companies': NAMES[:len(NAMES)-8], 'update': True})
    else:
        responses = Experience.objects.all().order_by('-id')[:3]
        return render(request, 'home.html', {'responses': responses})

@login_required()
def delete(request, id):
    try:
        response = Experience.objects.get(pk=id)
        username = response.user.username
        response.delete()
        return HttpResponseRedirect(reverse('profile',kwargs={'username':request.user.username}))
    except Experience.DoesNotExist:
        responses = Experience.objects.all().order_by('-id')[:3]
        return render(request, 'home.html', {'responses': responses})

@login_required()
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

@login_required()
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user , request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html',{'form':form})
