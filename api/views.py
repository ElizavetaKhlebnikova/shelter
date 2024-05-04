from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser

from pets.models import Pet
from pets.serializers import PetSerializer

class PetModelViewSet(ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'destroy'):
            self.permission_classes = (IsAdminUser, )
        return  super(PetModelViewSet, self).get_permissions()