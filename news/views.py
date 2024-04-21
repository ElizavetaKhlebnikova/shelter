from django.shortcuts import render
from django.views.generic.edit import CreateView
from .forms import CommonNewsForm, PetHistoryForm
from .tasks import send_news_task, send_pet_hystory_node_task
from .models import News, PetSubscriber
from pets.models import Pet
from users.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.shortcuts import HttpResponseRedirect
from common.views import TitleMixin
from django.views.generic.list import ListView


# Create your views here.

class AddNews(CreateView):
    template_name = 'news/add_news.html'
    form_class = CommonNewsForm
    success_url = reverse_lazy('news:add_news')

    def form_valid(self, form):
        """Проверяет валидность формы и отправляет на почту новости проекта"""
        if form.is_valid():
            news = form.save(commit=True)
            if news.send_news:
                news_id = news.id
                send_news_task.delay(news_id)
        return super().form_valid(form)


class PetHystory(CreateView):
    template_name = 'news/add_pet_hystory.html'
    form_class = PetHistoryForm
    success_url = reverse_lazy('news:add_pet_hystory')

    def form_valid(self, form):
        """Проверяет валидность формы и отправляет на почту новость о конкретном животном"""
        if form.is_valid():
            hystory_node = form.save(commit=True)
            if hystory_node.send_news:
                hystory_node_id = hystory_node.id
                send_pet_hystory_node_task.delay(hystory_node_id)
        return super().form_valid(form)


@login_required
def pet_follower_add(request, pet_id):
    """Проверяет наличие питомца в корзине пользователя и при его отсутствии добавляет питомца"""
    pet = Pet.objects.get(id=pet_id)
    pet_subscriber = PetSubscriber.objects.filter(user=request.user, pet=pet)
    if not pet_subscriber.exists():
        pet_subscriber.create(user=request.user, pet=pet)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


class MailingManagement(TitleMixin, ListView):
    model = Pet
    template_name = 'news/mailing_management.html'
    paginate_by = 8
    title = 'Happy vegan shelter - Управление почтовой рассылкой'

    def get_queryset(self):
        """Возвращает отфильтрованный список животных"""
        queryset = super(MailingManagement, self).get_queryset()
        queryset = [ps.pet for ps in PetSubscriber.objects.filter(user=self.request.user)]
        return queryset


@login_required
def pet_follower_remove(request, pet_id):
    """Удаляет корзину пользователя"""
    pet = Pet.objects.get(id=pet_id)
    pet_subscriber = PetSubscriber.objects.get(user=request.user, pet=pet)
    pet_subscriber.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def unsubscribe_from_all_news(request):
    user_id = request.user.id
    registrated_user = User.objects.filter(pk=user_id).update(common_news=False)
    pets_subscribes = PetSubscriber.objects.filter(user=request.user)
    pets_subscribes.delete()
    redirect_url = reverse('news:mailing_management')
    return HttpResponseRedirect(redirect_url)

def unsubscribe_from_all_news(request):
    user_id = request.user.id
    registrated_user = User.objects.filter(pk=user_id).update(common_news=False)
    pets_subscribes = PetSubscriber.objects.filter(user=request.user)
    pets_subscribes.delete()
    redirect_url = reverse('news:mailing_management')
    return HttpResponseRedirect(redirect_url)

def unsubscribe_from_common_news(request):
    user_id = request.user.id
    registrated_user = User.objects.filter(pk=user_id).update(common_news=False)
    redirect_url = reverse('news:mailing_management')
    return HttpResponseRedirect(redirect_url)

def unsubscribe_from_all_news_email(request, email):
    registrated_user = User.objects.filter(email=email)
    registrated_user.update(common_news=False)
    user = User.objects.get(email=email)
    pets_subscribes = PetSubscriber.objects.filter(user=user)
    pets_subscribes.delete()
    redirect_url = reverse('news:all_unsubscribe_success')
    return HttpResponseRedirect(redirect_url)

def unsubscribe_from_common_news_email(request, email):
    registrated_user = User.objects.filter(email=email).update(common_news=False)
    redirect_url = reverse('news:common_unsubscribe_success')
    return HttpResponseRedirect(redirect_url)

