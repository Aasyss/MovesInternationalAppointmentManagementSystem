from django.urls import path
from .views import book_appointment, appointment_success

urlpatterns = [
    path('book_appointment/', book_appointment, name='book_appointment'),
    path('success/', appointment_success, name='appointment_success'),
]
