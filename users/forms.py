from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)


from users.models import User, EmailVerification
# from users.tasks import send_email_verification
import uuid
from datetime import timedelta

from django.utils.timezone import now


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

    def save(self, commit=True):  #метод сохранения данных пользователя
        user = super(UserRegistrationForm, self).save(commit=True)
        expiration = now() + timedelta(hours=48)  # дата и время, когда код будет считаться недействительнам
        record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
        record.send_verification_email()
        return user



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
