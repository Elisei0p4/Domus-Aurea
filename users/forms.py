from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    # Определяем поля, которые мы хотим кастомизировать
    email = forms.EmailField(required=True, label="Email")
    first_name = forms.CharField(max_length=30, required=False, label="Имя")
    last_name = forms.CharField(max_length=30, required=False, label="Фамилия")

    class Meta(UserCreationForm.Meta):
        model = User
        # НОВЫЙ ПОРЯДОК ПОЛЕЙ. Пароли добавятся автоматически в конце.
        fields = ('first_name', 'last_name', 'email', 'username')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Словарь с плейсхолдерами для удобства
        placeholders = {
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'email': 'example@mail.com',
            'username': 'Придумайте логин', # Обновленный плейсхолдер
            'password1': 'Придумайте пароль',
            'password2': 'Повторите пароль',
        }

        # Применяем стили и плейсхолдеры ко ВСЕМ полям формы
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-input' # Гарантирует рамку для всех
            if field_name in placeholders:
                field.widget.attrs['placeholder'] = placeholders[field_name]
        
        # Обновляем названия полей (лейблы) на русский язык
        self.fields['username'].label = "Логин" # Обновленный лейбл
        self.fields['password1'].label = "Пароль"
        self.fields['password2'].label = "Подтверждение пароля"
        
        # Кастомизируем тексты-подсказки для лучшего вида
        self.fields['username'].help_text = 'Обязательное поле. Только буквы, цифры и символы @/./+/-/_.'
        self.fields['password1'].help_text = None # Убираем стандартный help_text, так как он будет в шаблоне
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