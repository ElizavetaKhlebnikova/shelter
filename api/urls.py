from django.urls import path, include
from rest_framework import routers

from .views import PetModelViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'pets', PetModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    ]
