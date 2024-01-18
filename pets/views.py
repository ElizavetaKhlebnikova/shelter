from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect, render, get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.core.cache import cache

from common.views import TitleMixin

from .models import Basket, Pet, PetsCategory


class IndexView(TitleMixin, TemplateView):
    template_name = 'pets/index.html'
    title = 'HappyVeganShelter'


class PetsListView(TitleMixin, ListView):  # за ListView зарезервировано название object_list
    model = Pet
    template_name = 'pets/pets.html'
    paginate_by = 4
    title = 'Store - Каталог'

    # вместо object_list можно задать context_object_name = ''

    def get_queryset(self):  # метод для получения данных из БД, с помощью которого можно также отфильтровать кверисет
        queryset = super(PetsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        pet_list = cache.get('pet_list' + str(category_id))
        if not pet_list:
            queryset = queryset.filter(category_id=category_id) if category_id != None else queryset
            cache.set('pet_list' + str(category_id), queryset, 60)
        else:
            queryset = pet_list
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):  # добавляем данные в контекст
        context = super(PetsListView, self).get_context_data()
        context['categories'] = PetsCategory.objects.all()
        context['category_id'] = self.kwargs.get(
            'category_id')  # передаётся id категории, которую мы выбрали, которая вынимается из кваргов при нажатии на ссылку
        return context


class PetView(TemplateView):
    template_name = 'pets/pet.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pet_name = kwargs['pet_name']
        feedback = Pet.objects.get(slug=pet_name)
        context['pet'] = feedback
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
