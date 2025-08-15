from django import forms

class PromoCodeForm(forms.Form):
    code = forms.CharField(
        label="Промокод",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-lavender-dark',
            'placeholder': 'Введите промокод'
        })
    )