from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from common.views import TitleMixin

from .forms import UserLoginForm, UserProfileForm, UserRegistrationForm, UserPasswordChangeForm
from .models import EmailVerification, User
from .tasks import send_email_verification, send_email_about_change_password_task
from .services.verification import change_parameter_of_the_user_object



class UserLoginView(LoginView):
    # не указываем модель, так как класс работает с моделью, указаанной в настройках в  переменной AUTH_USER_MODEL
    template_name = 'users/login.html'
    form_class = UserLoginForm


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Поздравляем! Вы успешно зарегистрированы!'
    title = 'HappyVeganShelter - Регистрация'

    def form_valid(self, form):
        """После проверки валидности формы сохраняет её и отправляет письмо для верификации пользователя"""
        if form.is_valid():
            feedback = form.save(commit=True)
            feedback_pk = feedback.pk
            send_email_verification.delay(feedback_pk)
        return super().form_valid(form)


class UserProfileView(TitleMixin, LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    login_url = reverse_lazy('users:login')
    success_url = reverse_lazy('users:profile')
    title = 'HappyVeganShelter - Личный кабинет'

    def get_object(self, queryset=None):
        '''Генерирует профиль на основании данных пользователя'''
        queryset = self.get_queryset()
        user = queryset.get(
            pk=self.request.user.id)
        return user


class EmailVerificationView(TitleMixin, TemplateView):
    title = 'HappyVeganShelter - подтверждение электронной почты'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):  # сюда прилетает code и email
        '''Извлекает код, пользователя и объект EmailVerification, проверяет наличие объекта EmailVerification
        и не истёк ли срок его действия'''
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user,
                                                               code=code)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            change_parameter_of_the_user_object(user)
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('/'))

class UserPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset_form.html'
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy("users:password_reset_done")


class UserPasswordChangeView(TitleMixin, PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('users:password_change_done')
    template_name = 'users/password_change.html'
    title = 'Смена пароля'

    def form_valid(self, form):
        """После проверки валидности формы сохраняет её и отправляет письмо для верификации пользователя"""
        if form.is_valid():
            feedback = form.save(commit=True)
            user_email = self.request.user.email
            send_email_about_change_password_task.delay(email=user_email)
        return super().form_valid(form)

class UserPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'users/password_change_done.html'



"""Тесты"""
