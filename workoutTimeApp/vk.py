import requests
from django.core.files.base import ContentFile
from datetime import datetime
from .models import CustomUser

def save_user_info(backend, user, response, *args, **kwargs):
    if backend.name == 'vk-oauth2':
        print("=== VK OAuth save_user_info called ===")
        print("VK Response keys:", response.keys())
        print("VK BDATE:", response.get('bdate'))

        email = response.get('email')
        full_name = response.get('first_name', '') + ' ' + response.get('last_name', '')
        birth_date = None

        bdate_str = response.get('bdate')
        if bdate_str:
            try:
                parts = bdate_str.split('.')
                if len(parts) == 3:
                    day, month, year = map(int, parts)
                    birth_date = datetime(year, month, day).date()  # Исправлено
                    print("Parsed birth_date:", birth_date)
            except Exception as e:
                print("❌ Ошибка парсинга даты рождения:", e)

        photo_url = response.get('photo_200')

        # Проверка на существующий email
        if email:
            try:
                existing_user = CustomUser.objects.get(email=email)
                # Если пользователь найден, привязываем его к текущему пользователю
                print("✅ Пользователь найден в базе данных:", existing_user)
                
                # Обновляем только те поля, которые пустые
                if not existing_user.full_name:
                    existing_user.full_name = full_name
                if not existing_user.birth_date and birth_date:
                    existing_user.birth_date = birth_date
                if not existing_user.profile_photo and photo_url:
                    try:
                        photo_response = requests.get(photo_url)
                        if photo_response.status_code == 200:
                            file_name = f"{existing_user.username}_vk.jpg"
                            existing_user.profile_photo.save(file_name, ContentFile(photo_response.content), save=False)
                    except Exception as e:
                        print("❌ Ошибка загрузки фото:", e)
                
                existing_user.save()
                print("✅ Данные пользователя обновлены (если нужно):", existing_user)
                return {'user': existing_user}
            except CustomUser.DoesNotExist:
                user.email = email

        # Если пользователь новый — заполняем остальные поля
        user.full_name = full_name
        if birth_date:
            user.birth_date = birth_date
        if photo_url:
            try:
                photo_response = requests.get(photo_url)
                if photo_response.status_code == 200:
                    file_name = f"{user.username}_vk.jpg"
                    user.profile_photo.save(file_name, ContentFile(photo_response.content), save=False)
            except Exception as e:
                print("❌ Ошибка загрузки фото (новый пользователь):", e)

        try:
            user.save()
            print("✅ Новый пользователь сохранён с birth_date:", user.birth_date)
        except Exception as e:
            print("❌ Ошибка при сохранении нового пользователя:", e)


def activate_user(strategy, details, user=None, *args, **kwargs):
    if user:
        # Устанавливаем пользователя как активного
        user.is_active = True
        user.save()