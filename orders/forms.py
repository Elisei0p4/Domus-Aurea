from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Иван'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Иванов'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'example@mail.com'}),
            'address': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'ул. Пушкина, д. 1, кв. 2'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '123456'}),
            'city': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Москва'}),
        }