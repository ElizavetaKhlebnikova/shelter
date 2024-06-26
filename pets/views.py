from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from common.views import TitleMixin

from .forms import RequestForGuardianshipForm
from .models import (Basket, Pet, PetHistory, PetImage, PetsCategory,
                     PetStatus)
from news.models import News, PetSubscriber
from .tasks import send_email_about_request_for_guardianship_task
from .services.changing_the_basket import create_or_update_the_basket


class IndexView(TitleMixin, TemplateView):
    template_name = 'pets/index.html'
    title = 'HappyVeganShelter'

    def get_context_data(self, **kwargs):
        """Возвращает в шаблон список объектов новостей"""
        context = super().get_context_data(**kwargs)
        context['news'] = cache.get_or_set('news', News.objects.order_by('index_number'), 30)
        return context


class DonationView(TitleMixin, TemplateView):
    template_name = 'pets/donation.html'
    title = 'HappyVeganShelter - моя помощь'

    def get_context_data(self, **kwargs):
        """Возвращает в шаблон объект range для отображения фотографий RabbitStones"""
        context = super().get_context_data(**kwargs)
        context['range'] = range(7)
        return context


class RequestForGuardianship(TitleMixin, CreateView):
    template_name = 'pets/request_for_guardianship_form.html'
    form_class = RequestForGuardianshipForm
    success_url = reverse_lazy('pets:request_for_guardianship_form_done')
    success_message = 'Ваша заявка успешно отправлена, ждите ответа!'
    title = 'HappyVeganShelter - заявка на опеку'

    def get_context_data(self, **kwargs):
        """Возвращает в шаблон список животных в соответствии с категорией"""
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs['category_id']
        pets = [pet.name for pet in Pet.objects.filter(category=category_id)]
        context['pet_list'] = ['не выбрано'] + pets
        context['category'] = PetsCategory.objects.get(pk=category_id)
        return context

    def form_valid(self, form):
        """Проверяет валидность формы и отправляет на почту информацию о запросе на опеку от пользователя"""
        if form.is_valid():
            feedback = form.save(commit=True)
            feedback_id = feedback.id
            send_email_about_request_for_guardianship_task.delay(feedback_id)
        return super().form_valid(form)


class PetsListView(TitleMixin, ListView):  # за ListView зарезервировано название object_list
    model = Pet
    template_name = 'pets/pets.html'
    paginate_by = 8
    title = 'HappyVeganShelter - животные'

    def get_queryset(self):
        """Возвращает отфильтрованный список животных"""
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

    def get_context_data(self, *, object_list=None, **kwargs):
        """Передаёт в контекст данные о категориях и статусах для фильтрации"""
        context = super(PetsListView, self).get_context_data()
        context['categories'] = PetsCategory.objects.all()
        context['statuses'] = PetStatus.objects.all()
        if self.request.user and self.request.user.id != None:
            user = self.request.user
            user_baskets = Basket.objects.filter(user=user)
            context['user_pet_id'] = [basket.pet_id for basket in user_baskets]
            user_pets = PetSubscriber.objects.filter(user=user)
            context['subscriber_pet_id'] = [pet.pet_id for pet in user_pets]
        return context


class PetView(TemplateView):
    template_name = 'pets/pet.html'

    def get_context_data(self, **kwargs):
        """Возвращает данные о питомце в соответствии с его слагом"""
        context = super().get_context_data(**kwargs)
        pet_name = kwargs['pet_name']
        context['pet'] = cache.get_or_set(f'pet {pet_name}', Pet.objects.get(slug=pet_name), 30)
        context['history'] = cache.get_or_set(f'history {pet_name}', PetHistory.objects.filter(pet=context['pet']), 30)
        context['images'] = cache.get_or_set(f'images {pet_name}', PetImage.objects.filter(pet=context['pet']), 30)
        return context


@login_required
def basket_add(request, pet_id):
    """добавляет питомца в любимцы пользователя"""
    create_or_update_the_basket(pet_id, request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, pet_id):
    """Удаляет корзину пользователя"""
    pet = Pet.objects.get(id=pet_id)
    basket = Basket.objects.get(user=request.user, pet=pet)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
