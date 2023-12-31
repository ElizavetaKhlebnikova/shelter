from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from common.views import TitleMixin

from .forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from .models import EmailVerification, User


class UserLoginView(LoginView):
    # не указываем модель, так как класс работает с моделью, указаанной в настройках в  переменной AUTH_USER_MODEL
    template_name = 'users/login.html'
    form_class = UserLoginForm



class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User  # куда сохраняем данные из формы
    form_class = UserRegistrationForm  # сама форма
    # fields = ['name', 'surname'] - поля, которые будут отображаться в форме
    template_name = 'users/registration.html'  # шаблон для отображения данных
    success_url = reverse_lazy('users:login')  # куда нужно перейти после сохранения данных
    success_message = 'Поздравляем! Вы успешно зарегистрированы!'
    title = 'HappyVeganShelter - Регистрация'



class UserProfileView(TitleMixin, LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    login_url = reverse_lazy('users:login')
    success_url = reverse_lazy('users:profile')
    title = 'HappyVeganShelter - Личный кабинет'

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        user = queryset.get(
            pk=self.request.user.id)  # вытаскиваем объект пользователя, по его primary key - это нужно для того, чтобы в роуте мы не прописывали pk (здесь он равен айдишнику)
        return user  # строим на основании данных юзера его профиль



class EmailVerificationView(TitleMixin, TemplateView):
    title = 'HappyVeganShelter - подтверждение электронной почты'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs): #сюда прилетает code и email
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code) #ищем оъект, соответствующий параметрам user, code
        if email_verifications.exists() and not email_verifications.first().is_expired():  #если таковой имеется, то:
            user.is_verified_email = True  #меняем данный параметр объекта пользователя
            user.save()    #сохраняем
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
            #возвращаем супер для отображения шаблона и срабатывания логики
        else:
            return HttpResponseRedirect(reverse('/'))