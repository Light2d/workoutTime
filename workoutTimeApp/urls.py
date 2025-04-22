from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import index, login, register, logout, last_event, sportgrounds, events, activate_account, profile, article, get_sportgrounds_data, events, event_detail, register_for_event
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', index, name='index'),
    path('events', events, name='events'),
    path('<int:event_id>/', event_detail, name='event_detail'),
    path('<int:event_id>/register/', register_for_event, name='register_for_event'),
    
    path('sportgrounds', sportgrounds, name='sportgrounds'),
    path('profile', profile, name='profile'),
    
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('', include('social_django.urls', namespace='social')),
    path('logout/', logout, name='logout'), 
    path('activate/<uuid:activation_code>/', activate_account, name='activate_account'),
    path('articles/<int:article_id>/', article, name='article'),
    path('sportgrounds/', sportgrounds, name='sportgrounds'),
    path('get_sportgrounds_data/', get_sportgrounds_data, name='get_sportgrounds_data'),
    path('last-event/', last_event, name='last_event'),

    
   path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:  # Только для режима разработки!
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)