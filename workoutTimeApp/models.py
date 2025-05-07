from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings
from tinymce.models import HTMLField

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True, verbose_name="Имя пользователя")
    first_name = models.CharField(max_length=150, blank=True, verbose_name="Имя")
    last_name = models.CharField(max_length=150, blank=True, verbose_name="Фамилия")
    email = models.EmailField(unique=False, verbose_name="Электронная почта")
    full_name = models.CharField(max_length=255, verbose_name="Полное имя")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    profile_photo = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="Аватар")
    activation_code = models.UUIDField(default=uuid.uuid4, editable=False, null=True, blank=True, unique=True, verbose_name="Код активации")
    is_active = models.BooleanField(default=False, verbose_name="Активен")
    is_registered = models.BooleanField(default=False, verbose_name="Зарегистрирован")

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_groups',
        blank=True,
        help_text='Группы, к которым принадлежит пользователь.',
        verbose_name='Группы',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions',
        blank=True,
        help_text='Права доступа пользователя.',
        verbose_name='Права доступа',
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'full_name']

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.is_active = True
        super().save(*args, **kwargs)

    def get_profile_photo(self):
        if self.profile_photo:
            return self.profile_photo.url
        return '/workoutTimeApp/static/imgs/profile/default.jpg'

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class TeamMember(models.Model):
    photo = models.ImageField(upload_to='team_photos/', verbose_name="Фото", blank=True, null=True)
    name = models.CharField(max_length=255, verbose_name="Имя")
    experience = models.PositiveIntegerField(verbose_name="Стаж (лет)")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Участник команды"
        verbose_name_plural = "Участники команды"


class LastEvent(models.Model):
    photo = models.ImageField(upload_to='lastEvent_photos/', verbose_name="Фото", blank=True, null=True)
    description = HTMLField(verbose_name="Описание поста", null=True)
    title = models.CharField(max_length=255, verbose_name="Название мероприятия")
    date = models.DateField(verbose_name="Дата")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Последнее мероприятие"
        verbose_name_plural = "Последние мероприятия"


class LastEventImage(models.Model):
    last_event = models.ForeignKey(LastEvent, related_name='images', on_delete=models.CASCADE, verbose_name="Мероприятие")
    image = models.ImageField(upload_to='last_event_images/', verbose_name="Изображение")

    def __str__(self):
        return f"Изображение для {self.last_event.title}"

    class Meta:
        verbose_name = "Изображение мероприятия"
        verbose_name_plural = "Изображения мероприятий"


class Article(models.Model):
    image = models.ImageField(upload_to='articles_images/', verbose_name="Изображение статьи")
    title = models.CharField(max_length=255, verbose_name="Название статьи")
    description = HTMLField(verbose_name="Описание статьи", null=True)
    date = models.DateField(verbose_name="Дата создания")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"


class SportGround(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    latitude = models.FloatField(verbose_name="Широта")
    longitude = models.FloatField(verbose_name="Долгота")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Спортивная площадка"
        verbose_name_plural = "Спортивные площадки"


class SportGroundImage(models.Model):
    sportground = models.ForeignKey(SportGround, on_delete=models.CASCADE, related_name="images", verbose_name="Площадка")
    image = models.ImageField(upload_to="sportground_images/", verbose_name="Изображение")

    def __str__(self):
        return f"Изображение для {self.sportground.name}"

    class Meta:
        verbose_name = "Изображение площадки"
        verbose_name_plural = "Изображения площадок"


class Event(models.Model):
    EVENT_TYPES = [
        ('competition', 'Соревнование'),
        ('masterclass', 'Мастер-класс'),
        ('archive', 'Архив'),
    ]

    title = models.CharField(max_length=255, verbose_name="Название")
    description = HTMLField(verbose_name="Описание", null=True)
    date = models.DateField(verbose_name="Дата")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    image = models.ImageField(upload_to='events/', verbose_name="Изображение")
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, verbose_name="Тип мероприятия")
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='events_participated', verbose_name="Участники")

    def is_past_event(self):
        from django.utils.timezone import now
        return self.date < now().date()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"

class Notification(models.Model):
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Уведомление для {self.recipient.username}: {self.message}"