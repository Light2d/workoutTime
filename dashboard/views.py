from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import EventForm, LastEventForm, ArticleForm, SportGroundForm, TeamMemberForm, CustomUserForm
from workoutTimeApp.models import Event, LastEvent, Article, SportGround, TeamMember, CustomUser, SportGroundImage
from .utils import admin_required
from django.urls import reverse
from django.contrib import messages
from django.db import IntegrityError, DatabaseError

@admin_required
def dashboard_home(request):
    return render(request, 'dashboard/dashboard.html')

from django.contrib import messages

def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('dashboard_home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            messages.success(request, 'Вы вошли в систему как администратор.')
            return redirect('dashboard_home')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль, либо у вас нет доступа.')

    return render(request, 'dashboard/login.html')


def admin_logout(request):
    logout(request)
    return redirect('admin_login')

def generate_crud_views(model, form_class, template_prefix, model_name_nominative, gender='m'):
    
    endings = {
        'm': {'add': 'добавлен', 'edit': 'обновлён', 'delete': 'удалён'},
        'f': {'add': 'добавлена', 'edit': 'обновлена', 'delete': 'удалена'},
        'n': {'add': 'добавлено', 'edit': 'обновлено', 'delete': 'удалено'}
    }
    
    @admin_required
    def list_view(request):
        objects = model.objects.all()
        return render(request, 'dashboard/list.html', {
            'objects': objects,
            'add_url': f'{template_prefix}_add',
            'edit_url': f'{template_prefix}_edit',
            'delete_url': f'{template_prefix}_delete',
            'model_name': model_name_nominative
        })

    @admin_required
    def add_view(request):
        form = form_class(request.POST or None, request.FILES or None)
        is_sportground = model.__name__.lower() == 'sportground'  # Проверка, является ли модель площадкой
        print(model.__name__.lower())
        if request.method == 'POST':
            if form.is_valid():
                try:
                    instance = form.save()

                    # Если добавляется площадка, обрабатываем изображения
                    if is_sportground:
                        images = request.FILES.getlist('images')  # "images" — имя поля в форме или input
                        for image in images:
                            SportGroundImage.objects.create(sportground=instance, image=image)

                    messages.success(request, f'{model_name_nominative.capitalize()} успешно {endings[gender]["add"]}.')
                    return redirect(reverse(f'{template_prefix}_list'))
                except (IntegrityError, DatabaseError) as e:
                    messages.error(request, f'Ошибка при добавлении: {str(e)}')
            else:
                messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')

        return render(request, 'dashboard/form.html', {'form': form, 'is_sportground': is_sportground})

    @admin_required
    def edit_view(request, pk):
        obj = get_object_or_404(model, pk=pk)
        form = form_class(request.POST or None, request.FILES or None, instance=obj)
        is_sportground = model.__name__.lower() == 'sportground'  # Проверка, является ли модель площадкой

        if request.method == 'POST':
            if form.is_valid():
                try:
                    instance = form.save()

                    # Если редактируется площадка, обрабатываем новые изображения
                    if is_sportground:
                        images = request.FILES.getlist('images')  # "images" — имя поля в форме или input
                        for image in images:
                            SportGroundImage.objects.create(sportground=instance, image=image)

                    messages.success(request, f'{model_name_nominative.capitalize()} успешно {endings[gender]["edit"]}.')
                    return redirect(reverse(f'{template_prefix}_list'))
                except (IntegrityError, DatabaseError) as e:
                    messages.error(request, f'Ошибка при сохранении: {str(e)}')
            else:
                messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')

        return render(request, 'dashboard/form.html', {'form': form, 'is_sportground': is_sportground})

    @admin_required
    def delete_view(request, pk):
        try:
            obj = get_object_or_404(model, pk=pk)
            obj.delete()
            messages.success(request, f'{model_name_nominative.capitalize()} успешно {endings[gender]["delete"]}.')
        except Exception as e:
            messages.error(request, f'Ошибка при удалении: {str(e)}')
        return redirect(reverse(f'{template_prefix}_list'))

    return list_view, add_view, edit_view, delete_view

# Генерация представлений для каждой модели
user_list, user_add, user_edit, user_delete = generate_crud_views(
    CustomUser, CustomUserForm, 'users', 'пользователь', 'm'
)
event_list, event_add, event_edit, event_delete = generate_crud_views(
    Event, EventForm, 'events', 'событие', 'n'
)
last_event_list, last_event_add, last_event_edit, last_event_delete = generate_crud_views(
    LastEvent, LastEventForm, 'last_events', 'последнее событие', 'n'
)
article_list, article_add, article_edit, article_delete = generate_crud_views(
    Article, ArticleForm, 'articles', 'статья', 'f'
)
sportground_list, sportground_add, sportground_edit, sportground_delete = generate_crud_views(
    SportGround, SportGroundForm, 'sportgrounds', 'площадка', 'f'
)
teammember_list, teammember_add, teammember_edit, teammember_delete = generate_crud_views(
    TeamMember, TeamMemberForm, 'teammembers', 'участник команды', 'm'
)
