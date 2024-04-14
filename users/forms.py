from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm, PasswordChangeForm)

from users.models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control-cast',
        'placeholder': "Введите имя пользователя"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control-cast',
        'placeholder': "Введите пароль"
    }))

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control-cast',
        'placeholder': "Введите имя"
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control-cast',
        'placeholder': "Введите фамилию"
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control-cast',
        'placeholder': "Введите логин"
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control-cast',
        'placeholder': "Введите адрес электронной почты"
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control-cast',
        'placeholder': "Введите пароль"
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control-cast',
        'placeholder': "Повторите пароль"
    }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control-cast',
        'placeholder': "Введите имя"
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control-cast',
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control-cast',
        'readonly': True,
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control-cast',
        'readonly': True,
    }))
    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'custom-file-input-cast',
    }), required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'image', 'username', 'email')

class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Введите старый проль', widget=forms.PasswordInput(attrs={'class': 'form-control-cast'}))
    new_password1 = forms.CharField(label='Введите новый проль', widget=forms.PasswordInput(attrs={'class': 'form-control-cast'}))
    new_password2 = forms.CharField(label='Повторите новый проль', widget=forms.PasswordInput(attrs={'class': 'form-control-cast'}))