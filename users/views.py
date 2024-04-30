from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from common.views import TitleMixin

from .forms import UserLoginForm, UserProfileForm, UserRegistrationForm, UserPasswordChangeForm
from .models import EmailVerification, User
from pets.models import Pet
from news.models import PetSubscriber
from pets.models import Basket
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

    def get_context_data(self, *, object_list=None, **kwargs):
        """Передаёт в контекст данные о содержимом корзин и подписке на события в жизни животных"""
        context = super(UserProfileView, self).get_context_data()
        user = self.request.user
        user_baskets = Basket.objects.filter(user=user)
        context['user_pet_id'] = [basket.pet_id for basket in user_baskets]
        user_pets = PetSubscriber.objects.filter(user=user)
        context['subscriber_pet_id'] = [pet.pet_id for pet in user_pets]
        return context


class UserPetsView(TitleMixin, LoginRequiredMixin, ListView):
    model = Pet
    template_name = 'pets/baskets.html'
    paginate_by = 8
    title = 'Happy vegan shelter - мои любимцы'

    def get_queryset(self):
        """Возвращает отфильтрованный список животных"""
        queryset = super(UserPetsView, self).get_queryset()
        queryset = [ps.pet for ps in Basket.objects.filter(user=self.request.user)]
        return queryset


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
