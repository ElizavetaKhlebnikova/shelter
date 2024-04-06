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
from .forms import RequestForGuardianshipForm
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from .tasks import send_email_about_request_for_guardianship_task


from common.views import TitleMixin

from .models import Basket, Pet, PetsCategory, PetHistory, News, PetStatus, PetImage


class IndexView(TitleMixin, TemplateView):
    template_name = 'pets/index.html'
    title = 'HappyVeganShelter'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news'] = cache.get_or_set('news', News.objects.order_by('index_number'), 30)
        return context

class DonationView(TitleMixin, TemplateView):
    template_name = 'pets/donation.html'
    title = 'моя помощь'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['range'] = range(7)
        return context

class RequestForGuardianship(CreateView):
    """ Добавить в модель категорий фотки и показывать их в окне формы слева """
    template_name = 'pets/Guardianship.html'
    form_class = RequestForGuardianshipForm
    success_url = reverse_lazy('pets:my_help')  # куда нужно перейти после сохранения данных
    success_message = 'Ваша заявка успешно отправлена, ждите ответа!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs['category_id']
        pet_list = ['не выбрано']
        pets = [pet.name for pet in Pet.objects.filter(category=category_id)]
        context['pet_list'] = pet_list + pets
        return context
    def form_valid(self, form):
        if form.is_valid():
            feedback = form.save(commit=True)
            feedback_pk = feedback.pk
            send_email_about_request_for_guardianship_task.delay(feedback_pk)
        return super().form_valid(form)

class PetsListView(TitleMixin, ListView):  # за ListView зарезервировано название object_list
    model = Pet
    template_name = 'pets/pets.html'
    paginate_by = 9
    title = 'Store - Каталог'

    def get_queryset(self):
        queryset = super(PetsListView, self).get_queryset()
        category_id = self.request.GET.get('category')
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
        context['pet'] = cache.get_or_set('pet', Pet.objects.get(slug=pet_name), 30)
        context['history'] = cache.get_or_set('history', PetHistory.objects.filter(pet=context['pet']), 30)
        context['images'] = cache.get_or_set('images', PetImage.objects.filter(pet=context['pet']), 30)
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
