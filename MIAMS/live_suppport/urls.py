from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.start_chat, name='start_chat'),
    path('<int:support_group_id>/', views.start_chat, name='start_chat_group'),
    path('ajax/get_messages/', views.get_messages, name='get_messages'),
    re_path(r'^ajax/(?P<chat_id>\d+)/post_message/$', views.post_message, name='post_message'),
    re_path(r'^ajax/(?P<chat_id>\d+)/end_chat/$', views.end_chat, name='end_chat'),
    re_path(r'^ajax/(?P<chat_id>\d+)/join_chat/$', views.join_chat, name='join_chat'),
    re_path(r'^(?P<chat_uuid>[\w-]+)/end_chat/$', views.client_end_chat, name='client_end_chat'),
    re_path(r'^(?P<chat_uuid>[\w-]+)/get_messages/$', views.client_get_messages, name='client_get_messages'),
    re_path(r'^(?P<chat_uuid>[\w-]+)/post_message/$', views.client_post_message, name='client_post_message'),
    re_path(r'^(?P<chat_uuid>[\w-]+)/$', views.client_chat, name='client_chat'),
]
