from django import forms

from ads.models import Advert


class PostForm(forms.ModelForm):
    class Meta:
        model = Advert
        fields = ['title',
                  'category',
                  'content',
                  'upload'
                  ]


class AdvertForm(forms.ModelForm):
    class Meta:
        model = Advert
        fields = ['title', 'content', 'category']
        labels = {
            'title': 'Заголовок',
            'content': 'Текст объявления',
            'category': 'Категория'
        }