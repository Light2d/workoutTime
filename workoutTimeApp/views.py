from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import CustomRegistrationForm, CustomAuthenticationForm, ProfileForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
import uuid
from django.contrib.auth.decorators import login_required
from .models import TeamMember, LastEvent, CustomUser, Article, SportGround, SportGroundImage, Event
from django.http import JsonResponse
from django.utils.timezone import now
from datetime import timedelta

# Регистрация
def register(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Создаём пользователя, но не сохраняем сразу
            user.is_active = False  # Делаем пользователя неактивным
            user.activation_code = uuid.uuid4()  # Генерируем код активации
            user.save()  # Сохраняем пользователя с кодом активации
            send_activation_email(user)  # Отправляем письмо с кодом активации
            messages.success(request, 'На вашу почту отправлено письмо с подтверждением регистрации.')
            return redirect('login')
        else:
            messages.error(request, 'Ошибка в данных формы.')
    else:
        form = CustomRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})

# Авторизация
def login(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    form = CustomAuthenticationForm()
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        print(f"Form data: {request.POST}")  # Печать данных формы

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Неверное имя пользователя или пароль.')
        else:
            for error in form.errors.get('__all__', []):  # Достаем общие ошибки формы
                messages.error(request, error)  # Добавляем их в сообщения
            else:
                form = CustomAuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


def send_activation_email(user):
    activation_link = f"{settings.SITE_URL}/activate/{user.activation_code}/"
    subject = "Подтверждение регистрации"
    message = f"Здравствуйте, {user.username}!\n\nДля подтверждения регистрации перейдите по ссылке:\n{activation_link}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)


def activate_account(request, activation_code):
    user = get_object_or_404(CustomUser, activation_code=activation_code)

    if user.is_active:
        messages.warning(request, 'Аккаунт уже активирован.')
        return redirect('login')

    user.is_active = True
    print(user.activation_code)
    user.activation_code = None  
    user.save()

    messages.success(request, 'Ваш аккаунт успешно активирован! Теперь вы можете войти.')
    return redirect('login')

def logout(request):
    auth_logout(request)  
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('login')  


def index(request):
    team_members = TeamMember.objects.all()  
    last_event = LastEvent.objects.latest('date')  
    articles = Article.objects.all()
    return render(request, 'index.html', {'team_members': team_members, 'last_event': last_event, 'articles': articles})

@login_required
def article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'article.html', {'article': article})

@login_required
def profile(request):
    user = request.user

    if request.method == "POST":
        if "profile_photo" in request.FILES:
            user.profile_photo = request.FILES["profile_photo"]
            user.save()
            return JsonResponse({"status": "success", "photo_url": user.profile_photo.url})

        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileForm(instance=user)

    return render(request, "profile.html", {"user": user, "form": form})


def get_sportgrounds_data(request):
    sportgrounds = SportGround.objects.all()
    
    grounds_data = []
    for ground in sportgrounds:
        images = SportGroundImage.objects.filter(sportground=ground)
        grounds_data.append({
            "name": ground.name,
            "address": ground.address,
            "latitude": ground.latitude,
            "longitude": ground.longitude,
            "images": [image.image.url for image in images]
        })
    
    return JsonResponse(grounds_data, safe=False)

@login_required
def sportgrounds(request):
    return render(request, 'sportgrounds.html')


@login_required
def events(request):
    # Получаем все события
    competitions = Event.objects.filter(event_type='competition')
    masterclasses = Event.objects.filter(event_type='masterclass')
    archive = Event.objects.filter(event_type='archive')

    # Проверяем и обновляем статус событий
    for event in competitions | masterclasses:
        if event.date < now().date() - timedelta(days=2):  # Если прошло 2 дня
            event.event_type = 'archive'
            event.save()

    return render(request, 'events.html', {
        'competitions': competitions,
        'masterclasses': masterclasses,
        'archive': archive
    })

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'event_detail.html', {'event': event})

@login_required
def register_for_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if event.is_past_event():
        messages.error(request, "Регистрация на это мероприятие закрыта.")
        return redirect('event_detail', event_id=event.id)

    if request.user in event.participants.all():
        messages.warning(request, "Вы уже зарегистрированы на это мероприятие.")
    else:
        event.participants.add(request.user)
        messages.success(request, "Вы успешно зарегистрировались!")

    return redirect('event_detail', event_id=event.id)
