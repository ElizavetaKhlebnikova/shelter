from rest_framework import serializers

from pets.models import Pet, PetsCategory, PetStatus, Basket


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

class BasketSerializer(serializers.ModelSerializer):
    pet = PetSerializer()
    class Meta:
        model = Basket
        fields = ("id", "pet", "created_timestamp")
        read_only_fields = ('created_timestamp', )