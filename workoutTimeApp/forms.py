from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from .models import Event


CustomUser = get_user_model()

# Кастомная форма для регистрации
class CustomRegistrationForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'registration__input',
            'placeholder': 'Введите ваше ФИО'
        })
    )
    username = forms.CharField(
        required=True,
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'registration__input',
            'placeholder': 'Введите имя пользователя'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'registration__input',
            'placeholder': 'Введите ваш email'
        })
    )
    birth_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            'class': 'registration__input',
            'placeholder': 'Введите вашу дату рождения (ГГГГ-ММ-ДД)',
            'type': 'date'
        })
    )
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'registration__input',
            'placeholder': 'Введите пароль'
        })
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'registration__input',
            'placeholder': 'Повторите пароль'
        })
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'full_name', 'email', 'birth_date', 'password1', 'password2']
        
    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if len(full_name.split()) < 2:
            raise ValidationError('Полное имя должно содержать хотя бы имя и фамилию.')
        return full_name

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date >= timezone.now().date():
            raise ValidationError('Дата рождения не может быть в будущем.')
        return birth_date


    # Кастомизация сообщений для существующего имени пользователя и email
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError('Пользователь с таким именем уже существует.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует.')
        return email
    
    
    
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'login__input',
            'placeholder': 'Введите ваше имя пользователя'
        }),
        label="Имя пользователя"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'login__input',
            'placeholder': 'Введите пароль'
        }),
        label="Пароль"
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        print(f"Username cleaned: {username}")  # Отладка
        if not username:
            raise forms.ValidationError("Username is required.")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        print(f"Password cleaned: {password}")  # Отладка
        if not password:
            raise forms.ValidationError("Password is required.")
        return password


class CustomPasswordResetForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
        'class': 'login__input',
        'placeholder': 'Введите ваш email'
        }),
        label="Email"
        )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email
    

class CustomSetPasswordForm(forms.Form):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'login__input',  # Добавляем класс сюда
            'placeholder': 'Введите новый пароль'
        }),
        label="Новый пароль"
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'login__input',  # Добавляем класс сюда
            'placeholder': 'Повторите новый пароль'
        }),
        label="Подтвердите новый пароль"
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")

        if password1 and password2 and password1 != password2:
            self.add_error('new_password2', "Пароли не совпадают.")
        return cleaned_data


class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = []