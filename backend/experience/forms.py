from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserCreateForm(UserCreationForm):
    class Meta:
        fields =('first_name','last_name','email','password1','password2')
        model = User