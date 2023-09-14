from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
from django.conf import settings

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('set_availability/', views.set_availability, name='set_availability'),
]