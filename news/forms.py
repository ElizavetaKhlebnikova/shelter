from django import forms

from .models import News
from pets.models import PetHistory
import datetime
from django.forms.widgets import NumberInput


class CommonNewsForm(forms.ModelForm):
    image = forms.ImageField(label='Фото*',widget=forms.FileInput(attrs={
        'class': 'custom-file-input-cast',
    }), required=False)

    class Meta:
        model = News
        fields = ['index_number', 'title', 'text', 'image', 'image_url', 'connection', 'pet', 'send_news']

    def __init__(self, *args, **kwargs):
        super(CommonNewsForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['connection'].widget.attrs.update({'class': 'form-control-cast-new'})
        self.fields['send_news'].widget.attrs.update({'class': 'form-control-cast-new'})
        self.fields['pet'].widget.attrs.update({'class': 'form-select'})


class PetHistoryForm(forms.ModelForm):
    date = forms.DateField(label='Примерная дата события*', widget=NumberInput(attrs={'type': 'date'}))
    class Meta:
        model = PetHistory
        fields = ['title', 'date', 'pet', 'node', 'send_news']

    def __init__(self, *args, **kwargs):
        super(PetHistoryForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['pet'].widget.attrs.update({'class': 'form-select'})
        self.fields['send_news'].widget.attrs.update({'class': 'form-control-cast-new'})
