from .models import Category, Advert
from django.forms import DateTimeInput
from django_filters import FilterSet, CharFilter, ModelChoiceFilter
from django.db.models import Q
from django import template

register = template.Library()


@register.filter
def is_author(user):
    """
    Custom template filter to check if a user is an author.

    Args:
        user (User): The user to check.

    Returns:
        bool: True if the user is an author, False otherwise.
    """
    return user.groups.filter(name='Авторы').exists()


class AdvertFilter(FilterSet):
    """
    FilterSet class for filtering the Advert model.
    """

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
        """
        Custom method for filtering based on the created_at field.

        Args:
            queryset (QuerySet): The initial queryset.
            name (str): The field name.
            value (str): The filter value.

        Returns:
            QuerySet: The filtered queryset.
        """
        return queryset.filter(Q(**{f'{name}__gt': value}) | Q(**{f'{name}__isnull': True}))

    class Meta:
        model = Advert
        fields = []
