from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser, Group, Permission


class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)  # Уникальный email
    birth_date = models.DateField()
    activation_code = models.UUIDField(default=uuid.uuid4, editable=False, null=True, blank=True, unique=True)  # Код активации
    is_active = models.BooleanField(default=False)  # Активность пользователя
    
    USERNAME_FIELD = 'username'  # Для входа используется username
    REQUIRED_FIELDS = ['email', 'full_name', 'birth_date']  # Для создания пользователя требуются email и другие поля

    def save(self, *args, **kwargs):
        if self.is_superuser:  # Если это суперпользователь
            self.is_active = True  # Устанавливаем is_active в True
        super().save(*args, **kwargs)  # Вызов стандартного метода save

    # Обновленный related_name для groups
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_groups',  # Уникальное имя для related_name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    # Обновленный related_name для user_permissions
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions',  # Уникальное имя для related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    
    def __str__(self):
        return self.username