from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('company/',views.company,name='company'),
    path('experience/',views.experience,name='experience'),
    path('write/', views.write, name='write'),
    path('about/', views.about, name='about'),
]
