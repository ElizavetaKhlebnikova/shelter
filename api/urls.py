from django.urls import path, include
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView

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
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("schema/redoc/", SpectacularRedocView.as_view(url_name="api:schema"), name="redoc")
]
