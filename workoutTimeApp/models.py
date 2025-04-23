from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.postgres.fields import ArrayField 
from django.conf import settings
from tinymce.models import HTMLField


class CustomUser(AbstractUser):
    profile_photo = models.ImageField(upload_to='avatars/', null=True, blank=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=False)  
    birth_date = models.DateField(null=True, blank=True) 
    activation_code = models.UUIDField(default=uuid.uuid4, editable=False, null=True, blank=True, unique=True)  # Код активации
    is_active = models.BooleanField(default=False) 
    
    is_registered = models.BooleanField(default=False)

    
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
    
    def get_profile_photo(self):
        if self.profile_photo:
            return self.profile_photo.url
        return '/workoutTimeApp/static/imgs/profile/default.jpg'  
    
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
    description = HTMLField(verbose_name="Описание поста", null="true")
    title = models.CharField(max_length=255, verbose_name="Название мероприяти") 
    date = models.DateField()  

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Последнее мероприятие"
        verbose_name_plural = "Последнее мероприятие"
        
class LastEventImage(models.Model):
    last_event = models.ForeignKey(LastEvent, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='last_event_images/')

class Article(models.Model):
    image = models.ImageField(upload_to='articles_images/', verbose_name="Изображение поста")
    title = models.CharField(max_length=255, verbose_name="Название поста")
    description = HTMLField(verbose_name="Описание поста", null="true")
    date = models.DateField(verbose_name="Дата создания")  

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
    
    
class Event(models.Model):
    EVENT_TYPES = [
        ('competition', 'Соревнование'),
        ('masterclass', 'Мастер-класс'),
        ('archive', 'Архив'),
    ]
    
    title = models.CharField(max_length=255)
    description = HTMLField(verbose_name="Описание", null="true")
    date = models.DateField()
    address = models.CharField(max_length=255)
    image = models.ImageField(upload_to='events/')
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='events_participated')

    def is_past_event(self):
        from django.utils.timezone import now
        return self.date < now().date()

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Мероприятие" 
        verbose_name_plural = "Мероприятие"