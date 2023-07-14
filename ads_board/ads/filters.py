from .models import Category, Advert

from django.forms import DateTimeInput
from django_filters import FilterSet, CharFilter, ModelChoiceFilter
from django.db.models import Q


from django import template

register = template.Library()


@register.filter
def is_author(user):
    return user.groups.filter(name='Авторы').exists()


class AdvertFilter(FilterSet):
    add_title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Заголовок'
    )
    add_category = ModelChoiceFilter(
        field_name='category',
        queryset=Category.objects.all(),
        label='Категория поста',
        empty_label='Select a category'
    )
    add_date = CharFilter(
        field_name='created_at',
        method='filter_created_at',
        label='Дата публикации',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    def filter_created_at(self, queryset, name, value):
        return queryset.filter(Q(**{f'{name}__gt': value}) | Q(**{f'{name}__isnull': True}))

    class Meta:
        model = Advert
        fields = []
