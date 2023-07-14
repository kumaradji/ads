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
