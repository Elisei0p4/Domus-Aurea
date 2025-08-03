import django_filters
from django import forms
from .models import Product

class ProductFilter(django_filters.FilterSet):
    SORT_CHOICES = (
        ('name', 'По названию (А-Я)'),
        ('-name', 'По названию (Я-А)'),
        ('final_price', 'Сначала дешевые'),
        ('-final_price', 'Сначала дорогие'),
        ('-created', 'Сначала новинки'),
    )
    ordering = django_filters.ChoiceFilter(
        label='Сортировка', 
        choices=SORT_CHOICES, 
        method='filter_by_order',
        widget=forms.Select(attrs={'class': 'filter-select'})
    )

    min_price = django_filters.NumberFilter(field_name='final_price', lookup_expr='gte', widget=forms.NumberInput(attrs={'placeholder': 'от', 'class': 'filter-input-range'}))
    max_price = django_filters.NumberFilter(field_name='final_price', lookup_expr='lte', widget=forms.NumberInput(attrs={'placeholder': 'до', 'class': 'filter-input-range'}))
    
    class Meta:
        model = Product
        fields = ['min_price', 'max_price', 'ordering']

    def filter_by_order(self, queryset, name, value):
        return queryset.order_by(value)