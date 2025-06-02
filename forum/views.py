from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ForumThread, ForumPost
from .forms import ForumThreadForm, ForumPostForm
from workoutTimeApp.models import Notification

class ForumThreadListView(ListView):
    model = ForumThread
    template_name = 'forum/thread_list.html'
    context_object_name = 'threads'


class ForumThreadDetailView(LoginRequiredMixin, DetailView):
    model = ForumThread
    template_name = 'forum/thread_detail.html'
    context_object_name = 'thread'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ForumPostForm()
        context['posts'] = self.object.posts.filter(parent=None)  # корневые посты
        context['notifications'] = Notification.objects.filter(recipient=self.request.user, is_read=False)
        return context

    def get_post_depth(self, post):
        depth = 0
        while post.parent:
            depth += 1
            post = post.parent
        return depth

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not request.user.is_authenticated:
            return redirect('login')

        form = ForumPostForm(request.POST)
        parent_post = None

        if 'parent' in request.POST:
            parent_post = get_object_or_404(ForumPost, id=request.POST['parent'])

            # Ограничение вложенности до 3 уровней (реализовано как до 2)
            if self.get_post_depth(parent_post) >= 1:
                parent_post = parent_post.parent

        if form.is_valid():
            post = form.save(commit=False)
            post.thread = self.object
            post.author = request.user
            if parent_post:
                post.parent = parent_post
            post.save()

            # Уведомление автору, на чей пост ответили
            if post.parent:
                recipient = post.parent.author
                if recipient != request.user:
                    Notification.objects.create(
                        recipient=recipient,
                        message=f"{request.user.username} ответил(а) на ваш пост в теме «{self.object.title}».",
                    )
            else:
                # Ответ на сам вопрос (корневой пост), уведомляем его автора
                root_post = self.object.posts.filter(parent=None).first()
                if root_post and root_post.author != request.user:
                    Notification.objects.create(
                        recipient=root_post.author,
                        message=f"{request.user.username} ответил(а) на ваш вопрос в теме «{self.object.title}».",
                    )

        return redirect('forum:thread_detail', pk=self.object.pk)



class ForumThreadCreateView(LoginRequiredMixin, CreateView):
    model = ForumThread
    form_class = ForumThreadForm
    template_name = 'forum/thread_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
