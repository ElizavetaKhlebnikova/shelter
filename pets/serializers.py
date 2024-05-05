from rest_framework import serializers

from pets.models import Pet, PetsCategory, PetStatus, Basket, RequestForGuardianship, OtherPet


class PetSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', queryset=PetsCategory.objects.all())
    status = serializers.SlugRelatedField(slug_field='status', queryset=PetStatus.objects.all())

    class Meta:
        model = Pet
        fields = ('id', 'name', 'description', 'image', 'category',
                  'is_hospitalized', 'gender', 'status')


class BasketSerializer(serializers.ModelSerializer):
    pet = PetSerializer()

    class Meta:
        model = Basket
        fields = ("id", "pet", "created_timestamp")
        read_only_fields = ('created_timestamp',)


class RequestForGuardianshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestForGuardianship
        fields = ('id', 'user_name', 'email', 'pet', 'city', 'created',
                  'goal', 'other_pets', 'other_pet', 'conditions')
        read_only_fields = ('created', )