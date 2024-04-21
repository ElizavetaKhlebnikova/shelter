from django.urls import path
from django.views.generic.base import TemplateView
from . import views

app_name = 'news'
urlpatterns = [
    path('add_news/', views.AddNews.as_view(), name='add_news'),
    path('add_pet_hystory/', views.PetHystory.as_view(), name='add_pet_hystory'),
    path('pet_follower/add/<int:pet_id>', views.pet_follower_add, name='pet_follower_add'),
    path('pet_follower/remove/<int:pet_id>', views.pet_follower_remove, name='pet_follower_remove'),
    path('mailing_management/', views.MailingManagement.as_view(), name='mailing_management'),
    path('unsubscribe_from_all_news/', views.unsubscribe_from_all_news, name='unsubscribe_from_all_news'),
    path('unsubscribe_from_common_news/', views.unsubscribe_from_common_news, name='unsubscribe_from_common_news'),
    path('unsubscribe_from_all_news/<str:email>/', views.unsubscribe_from_all_news_email, name='unsubscribe_from_all_news_email'),
    path('unsubscribe_from_common_news/<str:email>/', views.unsubscribe_from_common_news_email, name='unsubscribe_from_common_news_email'),
    path('all_unsubscribe_success/', TemplateView.as_view(template_name='news/all_unsubscribe_success.html'), name='all_unsubscribe_success'),
    path('common_unsubscribe_success/', TemplateView.as_view(template_name='news/common_unsubscribe_success.html'), name='common_unsubscribe_success'),
   ]
