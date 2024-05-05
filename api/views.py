from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from pets.models import Pet, Basket
from pets.serializers import PetSerializer, BasketSerializer

class PetModelViewSet(ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'destroy'):
            self.permission_classes = (IsAdminUser, )
        return  super(PetModelViewSet, self).get_permissions()

class BascketModelViewSet(ModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = None

    def get_queryset(self):
        queryset = super(BascketModelViewSet, self).get_queryset()
        return queryset.filter(user=self.request.user)
