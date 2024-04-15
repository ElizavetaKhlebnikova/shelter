from django.shortcuts import render
from django.views.generic.edit import CreateView
from .forms import CommonNewsForm, PetHistoryForm
from .tasks import send_news_task, send_pet_hystory_node_task
from .models import News

from django.urls import reverse_lazy

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
