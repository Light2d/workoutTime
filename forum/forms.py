from django import forms
from .models import ForumThread, ForumPost

class ForumThreadForm(forms.ModelForm):
    class Meta:
        model = ForumThread
        fields = ['title', 'content']


class ForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ['content']

    def __init__(self, *args, **kwargs):
        # Если передан родительский пост, добавляем его в форму.
        self.parent_post = kwargs.pop('parent_post', None)
        super().__init__(*args, **kwargs)
