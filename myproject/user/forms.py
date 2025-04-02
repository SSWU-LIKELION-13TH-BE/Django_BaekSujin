from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True) #이메일 필수
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']