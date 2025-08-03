from django import forms
from .models import Review, ContactMessage

class ProductFilterForm(forms.Form):
    SORT_CHOICES = (
        ('name_asc', 'По названию (А-Я)'),
        ('name_desc', 'По названию (Я-А)'),
        ('price_asc', 'Сначала дешевые'),
        ('price_desc', 'Сначала дорогие'),
        ('created_desc', 'Сначала новинки'),
    )
    
    min_price = forms.DecimalField(
        label='Цена от', 
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': '0', 'class': 'filter-input'})
    )
    max_price = forms.DecimalField(
        label='Цена до', 
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': '100000', 'class': 'filter-input'})
    )
    ordering = forms.ChoiceField(
        label='Сортировать', 
        choices=SORT_CHOICES, 
        required=False,
        widget=forms.Select(attrs={'class': 'filter-select'})
    )

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.Select(choices=[(i, str(i)) for i in range(1, 6)], attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-lavender-dark'
            }),
            'text': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-lavender-dark',
                'rows': 4,
                'placeholder': 'Поделитесь своим мнением о товаре...'
            })
        }
        labels = {
            'rating': 'Ваша оценка',
            'text': 'Текст отзыва'
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ваше имя', 'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Ваш Email', 'class': 'form-input'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Тема сообщения', 'class': 'form-input'}),
            'message': forms.Textarea(attrs={'placeholder': 'Ваше сообщение...', 'rows': 5, 'class': 'form-input'}),
        }