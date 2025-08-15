from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'email': 'example@mail.com',
        }
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-input'
            if field_name in placeholders:
                field.widget.attrs['placeholder'] = placeholders[field_name]


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    first_name = forms.CharField(max_length=30, required=False, label="Имя")
    last_name = forms.CharField(max_length=30, required=False, label="Фамилия")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        placeholders = {
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'email': 'example@mail.com',
            'username': 'Придумайте логин',
            'password1': 'Придумайте пароль',
            'password2': 'Повторите пароль',
        }

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-input'
            if field_name in placeholders:
                field.widget.attrs['placeholder'] = placeholders[field_name]
        
        self.fields['username'].label = "Логин"
        self.fields['password1'].label = "Пароль"
        self.fields['password2'].label = "Подтверждение пароля"
        
        self.fields['username'].help_text = 'Обязательное поле. Только буквы, цифры и символы @/./+/-/_.'
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = 'Для подтверждения введите, пожалуйста, пароль ещё раз.'


    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:outline-none focus:border-lavender-dark',
        'placeholder': 'Имя пользователя',
        'autofocus': True
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:outline-none focus:border-lavender-dark',
        'placeholder': 'Пароль'
    }))