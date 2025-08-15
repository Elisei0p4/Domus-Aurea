import django_filters
from django import forms
from .models import Product, Category

class ProductFilter(django_filters.FilterSet):
    SORT_CHOICES = (
        ('name', 'По названию (А-Я)'),
        ('-name', 'По названию (Я-А)'),
        ('final_price', 'Сначала дешевые'),
        ('-final_price', 'Сначала дорогие'),
        ('-created', 'Сначала новинки'),
    )
    
    # Фильтр по бренду. Используем ModelChoiceFilter для создания выпадающего списка
    # из существующих брендов.
    brand = django_filters.ChoiceFilter(
        choices=[], # Будет заполнено в __init__
        field_name='brand',
        label='Бренд',
        empty_label='Все бренды',
        widget=forms.Select(attrs={'class': 'w-full border-gray-300 rounded-md shadow-sm focus:border-lavender-dark focus:ring-lavender-dark'})
    )

    ordering = django_filters.ChoiceFilter(
        label='Сортировка', 
        choices=SORT_CHOICES, 
        method='filter_by_order',
        widget=forms.Select(attrs={'class': 'w-full border-gray-300 rounded-md shadow-sm focus:border-lavender-dark focus:ring-lavender-dark'})
    )

    min_price = django_filters.NumberFilter(
        field_name='final_price', 
        lookup_expr='gte', 
        widget=forms.NumberInput(attrs={'placeholder': 'от', 'class': 'w-full border-gray-300 rounded-md shadow-sm focus:border-lavender-dark focus:ring-lavender-dark'})
    )
    max_price = django_filters.NumberFilter(
        field_name='final_price', 
        lookup_expr='lte', 
        widget=forms.NumberInput(attrs={'placeholder': 'до', 'class': 'w-full border-gray-300 rounded-md shadow-sm focus:border-lavender-dark focus:ring-lavender-dark'})
    )
    
    class Meta:
        model = Product
        fields = ['brand', 'min_price', 'max_price', 'ordering']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        brands = self.queryset.exclude(brand__isnull=True).exclude(brand__exact='') \
                       .values_list('brand', 'brand').distinct().order_by('brand')
        self.filters['brand'].extra['choices'] = brands

    def filter_by_order(self, queryset, name, value):
        return queryset.order_by(value)