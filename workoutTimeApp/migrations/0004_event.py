# Generated by Django 5.1.7 on 2025-03-21 09:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workoutTimeApp', '0003_customuser_profile_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('date', models.DateField()),
                ('address', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='events/')),
                ('event_type', models.CharField(choices=[('competition', 'Соревнование'), ('masterclass', 'Мастер-класс'), ('archive', 'Архив')], max_length=20)),
                ('participants', models.ManyToManyField(blank=True, related_name='events_participated', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
