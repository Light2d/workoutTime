from django.urls import path
from . import views

app_name = 'forum' 

urlpatterns = [
    path('', views.ForumThreadListView.as_view(), name='thread_list'),
    path('thread/<int:pk>/', views.ForumThreadDetailView.as_view(), name='thread_detail'),
    path('thread/new/', views.ForumThreadCreateView.as_view(), name='thread_create'),
]
