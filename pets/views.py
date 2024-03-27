import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect, render, get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.core.cache import cache
from django.core.mail import send_mail
from .filters import PetFilter
from requests import get
from .forms import RequestForCatGuardianshipForm, RequestForDogGuardianshipForm, RequestForRabbitGuardianshipForm
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy


from common.views import TitleMixin

from .models import Basket, Pet, PetsCategory, PetHistory, News, PetStatus, PetImage


class IndexView(TitleMixin, TemplateView):
    template_name = 'pets/index.html'
    title = 'HappyVeganShelter'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        feedback = News.objects.order_by('index_number')
        context['news'] = feedback
        context['news_len'] = len(feedback)
        return context

class DonationView(TitleMixin, TemplateView):
    template_name = 'pets/donation.html'
    # form_class = CatGuardianshipForm
    # success_url = reverse_lazy('pets:help')  # куда нужно перейти после сохранения данных
    # success_message = 'Поздравляем! Вы успешно зарегистрированы!'
    title = 'моя помощь'

class RequestForCatGuardianship(TitleMixin, CreateView):
    template_name = 'pets/CatGuardianship.html'
    form_class = RequestForCatGuardianshipForm
    success_url = reverse_lazy('pets:cat_guardianship')  # куда нужно перейти после сохранения данных
    success_message = 'Поздравляем! Вы успешно зарегистрированы!'
    title = 'моя помощь котам'
class RequestForDogGuardianship(TitleMixin, CreateView):
    template_name = 'pets/CatGuardianship.html'
    form_class = RequestForDogGuardianshipForm
    success_url = reverse_lazy('pets:cat_guardianship')  # куда нужно перейти после сохранения данных
    success_message = 'Поздравляем! Вы успешно зарегистрированы!'
    title = 'моя помощь котам'
class RequestForRabbitGuardianship(TitleMixin, CreateView):
    template_name = 'pets/CatGuardianship.html'
    form_class = RequestForRabbitGuardianshipForm
    success_url = reverse_lazy('pets:rabbit_guardianship')  # куда нужно перейти после сохранения данных
    success_message = 'Поздравляем! Вы успешно зарегистрированы!'
    title = 'моя помощь котам'



class PetsListView(TitleMixin, ListView):  # за ListView зарезервировано название object_list
    model = Pet
    template_name = 'pets/pets.html'
    paginate_by = 9
    title = 'Store - Каталог'

    def get_queryset(self):
        queryset = super(PetsListView, self).get_queryset()
        category_id = self.request.GET.get('category')
        # pet_list = cache.get('pet_list' + f'http://127.0.0.1:8003/pets/?category=1&gender=f&statuses=2')
        #
        # if not pet_list:
            # добавляем новые фильтры
        gender = self.request.GET.get('gender')
        status_id = self.request.GET.get('status')
        filters = {}
        if gender not in (None, '-'):
            filters['gender'] = gender
        if status_id not in (None, '-'):
            filters['status_id'] = status_id
        if category_id not in (None, '-'):
            filters['category_id'] = category_id
        if filter:
            queryset = queryset.filter(**filters)
            # cache.set('pet_list' + str(category_id), queryset, 60)
        # else:
        #     queryset = pet_list
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):  # добавляем данные в контекст
        context = super(PetsListView, self).get_context_data()
        context['categories'] = PetsCategory.objects.all()
        category_id = self.request.GET.get('category')
        context['statuses'] = PetStatus.objects.all()
        return context


class PetView(TemplateView):
    template_name = 'pets/pet.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pet_name = kwargs['pet_name']
        feedback = Pet.objects.get(slug=pet_name)
        history = PetHistory.objects.filter(pet=feedback)
        context['pet'] = feedback
        context['history'] = history
        images = PetImage.objects.filter(pet=feedback)
        context['images'] = images
        return context

@login_required
def basket_add(request, pet_id):
    pet = Pet.objects.all().get(id=pet_id)
    basket = Basket.objects.all().filter(user=request.user, pet=pet)

    if not basket.exists():
        basket.create(user=request.user, pet=pet)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
