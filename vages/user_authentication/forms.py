from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, TextInput, EmailInput


class UserForm(UserCreationForm):
    email = forms.EmailField(
        widget=EmailInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Your Email'
        })
    )
    username = forms.CharField(
        widget=TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Your Name'
        })
    )
    password1 = forms.CharField(
        widget=PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Password'
        })
    )
    password2 = forms.CharField(
        widget=PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Confirm Password'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Authentication (Login) Form
class UserLogin(AuthenticationForm):
    username = forms.CharField(
        widget=TextInput(attrs={
            'id': 'email',  # ID to match HTML input
            'class': 'form-control-custom',  # Custom class for styling
            'placeholder': 'Email'  # Placeholder text
        })
    )
    password = forms.CharField(
        widget=PasswordInput(attrs={
            'id': 'password',  # ID to match HTML input
            'class': 'form-control-custom',  # Custom class for styling
            'placeholder': 'Password'  # Placeholder text
        })
    )
