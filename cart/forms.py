from django import forms

class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'hidden', 'value': 1})
    )
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)