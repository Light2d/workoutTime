# Generated by Django 5.1.7 on 2025-03-28 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workoutTimeApp', '0004_event'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'verbose_name': 'Мероприятие', 'verbose_name_plural': 'Мероприятие'},
        ),
        migrations.AlterModelOptions(
            name='lastevent',
            options={'verbose_name': 'Последнее мероприятие', 'verbose_name_plural': 'Последнее мероприятие'},
        ),
        migrations.AlterField(
            model_name='customuser',
            name='profile_photo',
            field=models.ImageField(blank=True, null=True, upload_to='avatars/'),
        ),
    ]
