from django.urls import path
from django.views.decorators.cache import cache_page
from . import views

app_name = 'pets'
urlpatterns = [
    path('all_pets', views.PetsListView.as_view(), name='index'),
    path('my_help', views.DonationView.as_view(), name='help'),
    path('<int:category_id>', views.PetsListView.as_view(), name='category'),
    path('baskets/add/<int:pet_id>', views.basket_add, name='basket_add'),
    path('baskets/remove/<int:basket_id>', views.basket_remove, name='basket_remove'),
    path('pet/<slug:pet_name>', views.PetView.as_view(), name='one_pet'),
    path('cat_guardianship', views.RequestForCatGuardianship.as_view(), name='cat_guardianship'),
    path('dog_guardianship', views.RequestForDogGuardianship.as_view(), name='dog_guardianship'),
    path('rabbit_guardianship', views.RequestForRabbitGuardianship.as_view(), name='rabbit_guardianship'),
]
