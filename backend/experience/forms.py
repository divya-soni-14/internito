from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    class Meta:
        fields =('first_name','last_name','email','username','password1','password2')
        model = User
        