from django import forms
from .models import RequestForGuardianship, Pet, PetsCategory, OtherPets

class RequestForGuardianshipForm(forms.ModelForm):
    goals = (
        ('None', 'не выбрано'),
        ('foster care', 'передержка'),
        ('home', 'дом')
    )
    goal = forms.ChoiceField(choices=goals, label = "Кем вы готовы стать для животного?", widget=forms.Select())
    class Meta:
        model = RequestForGuardianship
        fields = ['user_name', 'email', 'pet', 'city', 'goal', 'other_pets', 'other_pet', 'conditions']
        widgets = {
            'other_pets': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(RequestForGuardianshipForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            if field != 'other_pet':
                field.widget.attrs.update({'class': 'form-control-cast',
                                       'placeholder': field.label})
            else:
                field.widget.attrs.update({'class': 'form-control-cast'})

class RequestForCatGuardianshipForm(RequestForGuardianshipForm):
    cats_id = PetsCategory.objects.get(name='Коты и кошки')
    pet_list = [('None', 'не выбрано')]
    pets = [(cat.name, cat.name) for cat in Pet.objects.filter(category=cats_id)]
    pet = forms.ChoiceField(choices=pet_list + pets, label = "Выберете питомца:", widget=forms.Select())

class RequestForDogGuardianshipForm(RequestForGuardianshipForm):
    cats_id = PetsCategory.objects.get(name='Собаки')
    pet_list = [('None', 'не выбрано')]
    pets = [(dog.name, dog.name) for dog in Pet.objects.filter(category=cats_id)]
    pet = forms.ChoiceField(choices=pet_list + pets, label="Выберете питомца:", widget=forms.Select())

class RequestForRabbitGuardianshipForm(RequestForGuardianshipForm):
    cats_id = PetsCategory.objects.get(name='Кролики')
    pet_list = [('None', 'не выбрано')]
    pets = [(rabbit.name, rabbit.name) for rabbit in Pet.objects.filter(category=cats_id)]
    pet = forms.ChoiceField(choices=pet_list + pets, label="Выберете питомца:", widget=forms.Select())