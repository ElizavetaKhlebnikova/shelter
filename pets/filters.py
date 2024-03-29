import django_filters
from .models import Pet


class PetFilter(django_filters.FilterSet):
    class Meta:
        model = Pet
        fields = ['category', 'status', 'gender']
