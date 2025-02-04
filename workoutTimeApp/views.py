from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import CustomRegistrationForm, CustomAuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
import uuid
from django.contrib.auth.decorators import login_required
from .models import TeamMember, LastEvent, CustomUser, Article, SportGround, SportGroundImage
from django.http import JsonResponse


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
                print(f"Authentication failed: Invalid credentials for username: {username}")
                messages.error(request, 'Неверное имя пользователя или пароль.')
        else:
            print(f"Form errors: {form.errors}")  # Печать ошибок формы
            print(f"Form errors JSON: {form.errors.as_json()}")  # Получаем ошибки формы в формате JSON
            messages.error(request, 'Форма не валидна.')
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


def article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'article.html', {'article': article})

@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})

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

def sportgrounds(request):
    return render(request, 'sportgrounds.html')


def events(request):
    return render(request, 'events.html')

def event(request):
    return render(request, 'event.html')

