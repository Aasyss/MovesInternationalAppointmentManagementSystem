from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('process_payment/<int:appointment_id>/<int:amount>/', views.process_payment, name='process_payment'),
    # Add other URL patterns as needed
]