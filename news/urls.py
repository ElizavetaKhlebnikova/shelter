from django.urls import path
from django.views.generic.base import TemplateView
from . import views

app_name = 'news'
urlpatterns = [
    path('add_news', views.AddNews.as_view(), name='add_news'),
   ]
