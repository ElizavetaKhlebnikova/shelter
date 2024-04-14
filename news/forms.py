from django import forms

from .models import News


class NewsForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'custom-file-input-cast',
    }), required=False)

    class Meta:
        model = News
        fields = ['index_number', 'title', 'text', 'image', 'image_url', 'connection', 'pet']

    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
                field.widget.attrs.update({'class': 'form-control-cast'})

