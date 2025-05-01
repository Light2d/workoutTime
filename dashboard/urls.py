from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),

    # CustomUser
    path('users/', views.user_list, name='users_list'),
    path('users/add/', views.user_add, name='users_add'),
    path('users/<int:pk>/edit/', views.user_edit, name='users_edit'),
    path('users/<int:pk>/delete/', views.user_delete, name='users_delete'),

    # Event
    path('events/', views.event_list, name='events_list'),
    path('events/add/', views.event_add, name='events_add'),
    path('events/<int:pk>/edit/', views.event_edit, name='events_edit'),
    path('events/<int:pk>/delete/', views.event_delete, name='events_delete'),

    # LastEvent
    path('last-events/', views.last_event_list, name='last_events_list'),
    path('last-events/add/', views.last_event_add, name='last_events_add'),
    path('last-events/<int:pk>/edit/', views.last_event_edit, name='last_events_edit'),
    path('last-events/<int:pk>/delete/', views.last_event_delete, name='last_events_delete'),

    # Article
    path('articles/', views.article_list, name='articles_list'),
    path('articles/add/', views.article_add, name='articles_add'),
    path('articles/<int:pk>/edit/', views.article_edit, name='articles_edit'),
    path('articles/<int:pk>/delete/', views.article_delete, name='articles_delete'),

    # SportGround
    path('sportgrounds/', views.sportground_list, name='sportgrounds_list'),
    path('sportgrounds/add/', views.sportground_add, name='sportgrounds_add'),
    path('sportgrounds/<int:pk>/edit/', views.sportground_edit, name='sportgrounds_edit'),
    path('sportgrounds/<int:pk>/delete/', views.sportground_delete, name='sportgrounds_delete'),

    # TeamMember
    path('team/', views.teammember_list, name='teammembers_list'),
    path('team/add/', views.teammember_add, name='teammembers_add'),
    path('team/<int:pk>/edit/', views.teammember_edit, name='teammembers_edit'),
    path('team/<int:pk>/delete/', views.teammember_delete, name='teammembers_delete'),
]
