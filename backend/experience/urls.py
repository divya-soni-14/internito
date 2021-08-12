from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('', views.home,name='home'),
    path('login/',views.signin,name='login'),
    path('logout/',auth_view.LogoutView.as_view(),name='logout'),
    path('register/',views.register,name='register'),
    path('company/',views.company,name='company'),
    path('experience/',views.experience,name='experience'),
    path('write/', views.write, name='write'),
    path('about/', views.about, name='about'),
    path('post/<int:id>', views.post, name='post'),
    path('profile/<username>', views.profile, name='profile'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('edit/<int:id>', views.edit, name='edit'),
    path('change_password/', views.change_password, name='change_password'),
    path('verifycode/<user>/',views.verifycode,name='verifycode'),
     path('password_reset/',views.password_reset_request,name='password_reset'),
    path('password_reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_view.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),
    path('feedback/',views.feedback,name='feedback'),
    path('feedback_reveive/',views.FeedbackReceive.as_view(),name='feedback_reveive')
]
