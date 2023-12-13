from django.urls import path
from django.views.decorators.cache import cache_page
from . import views

app_name = 'pets'
urlpatterns = [
    path('', views.PetsListView.as_view(), name='index'),
    path('category/<int:category_id>', views.PetsListView.as_view(), name='category'),
    path('page/<int:page>', views.PetsListView.as_view(), name='paginator'),
    path('baskets/add/<int:pet_id>', views.basket_add, name='basket_add'),
    path('baskets/remove/<int:basket_id>', views.basket_remove, name='basket_remove'),
]
