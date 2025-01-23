from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser  # Импорт вашей кастомной модели пользователя

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'full_name', 'email', 'birth_date', 'is_active', 'is_staff', 'date_joined', 'activation_code']
    list_filter = ['is_staff', 'is_active', 'date_joined']
    search_fields = ['username', 'full_name', 'email']
    ordering = ['date_joined']

    fieldsets = (
        (None, {
            'fields': ('username', 'full_name', 'email', 'password')
        }),
        ('Personal info', {
            'fields': ('birth_date',)
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Activation', {
            'fields': ('activation_code',)  # Добавляем поле для активации
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'full_name', 'email', 'password1', 'password2', 'birth_date', 'activation_code')
        }),
    )

    readonly_fields = ('activation_code',)  # Сделаем код активации только для чтения

    filter_horizontal = ('groups', 'user_permissions')

admin.site.register(CustomUser, CustomUserAdmin)
