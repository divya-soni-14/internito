from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('', views.home,name='home'),
    path('login/',auth_view.LoginView.as_view(template_name = 'login.html'),name='login'),
    path('logout/',auth_view.LogoutView.as_view(),name='logout'),
    path('register/',views.register,name='register'),
    path('company/',views.company,name='company'),
    path('experience/',views.experience,name='experience'),
    path('write/', views.write, name='write'),
    path('about/', views.about, name='about'),
    path('post/', views.post, name='post'),
    path('profile/', views.profile, name='profile'),
]
