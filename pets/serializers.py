from rest_framework import serializers

from pets.models import Pet, PetsCategory, PetStatus


class PetSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', queryset=PetsCategory.objects.all())
    status = serializers.SlugRelatedField(slug_field='status', queryset=PetStatus.objects.all())

    class Meta:
        model = Pet
        fields = ('id',
                 'name',
                 'description',
                 'image',
                 'category',
                 'is_hospitalized',
                 'gender',
                 'status')
