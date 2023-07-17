from django import forms
from ads.models import Advert


class PostForm(forms.ModelForm):
    """
    Form for creating and editing posts.
    """

    class Meta:
        model = Advert
        fields = ['title', 'category', 'content', 'upload']


class AdvertForm(forms.ModelForm):
    """
    Form for creating and editing adverts.
    """

    class Meta:
        model = Advert
        fields = ['title', 'content', 'category']
        labels = {
            'title': 'Заголовок',
            'content': 'Текст объявления',
            'category': 'Категория'
        }
