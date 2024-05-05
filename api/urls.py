from django.urls import path, include
from rest_framework import routers

from .views import (PetModelViewSet, BascketModelViewSet,
                    RequestForGuardianshipAPIView, RegisterView,
                    )

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'pets', PetModelViewSet)
router.register(r'baskets', BascketModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('request-for-guardianship/', RequestForGuardianshipAPIView.as_view()),
    path('register/', RegisterView.as_view()),
    ]
