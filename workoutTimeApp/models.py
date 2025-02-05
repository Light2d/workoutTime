from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.postgres.fields import ArrayField  # Для списка изображений (PostgreSQL)
from django.db.models import JSONField


class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)  # Уникальный email
    birth_date = models.DateField(null=True, blank=True) 
    profile_photo = models.URLField(null=True, blank=True)  # Поле для фото
    activation_code = models.UUIDField(default=uuid.uuid4, editable=False, null=True, blank=True, unique=True)  # Код активации
    is_active = models.BooleanField(default=False)  # Активность пользователя
    
    USERNAME_FIELD = 'username'  # Для входа используется username
    REQUIRED_FIELDS = ['email', 'full_name']  # Для создания пользователя требуются email и другие поля

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
    
    
class TeamMember(models.Model):
    photo = models.ImageField(upload_to='team_photos/', verbose_name="Фото", blank=True, null=True)  # Фото участника
    name = models.CharField(max_length=255, verbose_name="Имя")  # Имя участника
    experience = models.PositiveIntegerField(verbose_name="Стаж (лет)")  # Стаж в годах

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Участник команды"
        verbose_name_plural = "Участники команды"
        
        
class LastEvent(models.Model):
    photo = models.ImageField(upload_to='lastEvent_photos/', verbose_name="Фото", blank=True, null=True)  # Фото участника
    title = models.CharField(max_length=255, verbose_name="Название мероприяти") 
    date = models.DateField()  

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Последнее мероприятие"

class Article(models.Model):
    image = models.ImageField(upload_to='articles_images/', verbose_name="Изображение поста")
    title = models.CharField(max_length=255, verbose_name="Название поста")
    description = models.TextField(verbose_name="Описание поста")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        

class SportGround(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    def __str__(self):
        return self.name
    
    class Meta:
            verbose_name = "Спортивная площадка"
            verbose_name_plural = "Спортивные площадки"

class SportGroundImage(models.Model):
    sportground = models.ForeignKey(SportGround, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="sportground_images/")

    def __str__(self):
        return f"Image for {self.sportground.name}"
    