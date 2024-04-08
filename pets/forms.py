from django import forms

from .models import RequestForGuardianship


class RequestForGuardianshipForm(forms.ModelForm):
    goals = (
        ('None', 'не выбрано'),
        ('foster care', 'передержка'),
        ('home', 'дом')
    )
    goal = forms.ChoiceField(choices=goals, label="Кем вы готовы стать для животного?", widget=forms.Select())

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
