from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from social_core.exceptions import MissingBackend
from django.core.exceptions import ObjectDoesNotExist
from .models import CustomUser

def save_user_info(backend, user, response, *args, **kwargs):
    """Сохранить информацию о пользователе из ВКонтакте."""
    
    if backend.name == 'vk-oauth2':
        # Получаем email
        email = response.get('email')
        if email:
            user.email = email
        
        # Заполнение поля имени
        user.full_name = response.get('first_name', '') + ' ' + response.get('last_name', '')
        
        # Обработка даты рождения
        birth_date = response.get('bdate')
        if birth_date:
            try:
                # ВКонтакте может вернуть дату в формате 'DD.MM.YYYY'
                birth_date = birth_date.split('.')
                if len(birth_date) == 3:
                    user.birth_date = f"{birth_date[2]}-{birth_date[1]}-{birth_date[0]}"  # Преобразуем в формат YYYY-MM-DD
            except Exception as e:
                print(f"Ошибка при обработке даты рождения: {e}")
        
        # Получаем фото профиля
        photo = response.get('photo_200')
        if photo:
            user.profile_photo = photo  # предполагаем, что у вас есть поле profile_photo
        
        user.save()


def activate_user(strategy, details, user=None, *args, **kwargs):
    if user:
        # Устанавливаем пользователя как активного
        user.is_active = True
        user.save()