from django import forms

from ads.models import Advert


# Используется при новой публикации
class PostForm(forms.ModelForm):
    class Meta:
        model = Advert
        fields = ['title',
                  'category',
                  'content',
                  'upload'
                  ]


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)
