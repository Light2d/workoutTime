from django.db import models
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

class ForumThread(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок обсуждения")
    content = models.TextField(verbose_name="Описание вопроса")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='threads')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_absolute_url(self):
        return reverse('forum:thread_detail', kwargs={'pk': self.pk})
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответ"
        ordering = ['-created_at']
    


class ForumPost(models.Model):
    thread = models.ForeignKey(ForumThread, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(verbose_name="Ответ")
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Ответ от {self.author.username} на {self.thread.title}"

    def is_reply(self):
        return self.parent is not None

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
        ordering = ['created_at']
        
