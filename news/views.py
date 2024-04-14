from django.shortcuts import render
from django.views.generic.edit import CreateView
from .forms import NewsForm
from .tasks import send_news_task
from .models import News
from django.urls import reverse_lazy

# Create your views here.

class AddNews(CreateView):
    template_name = 'news/add_news.html'
    form_class = NewsForm
    success_url = reverse_lazy('news:add_news')

    def form_valid(self, form):
        """Проверяет валидность формы и отправляет на почту информацию о запросе на опеку от пользователя"""
        if form.is_valid():
            news = form.save(commit=True)
            news_id = news.id
            if News.objects.get(pk=news_id).pet == None:
                send_news_task.delay(news_id)
        return super().form_valid(form)
