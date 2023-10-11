from django.urls import path
from .views import book_appointment, appointment_success, appointment_failure, consultant_details
from payment.views import checkout

urlpatterns = [

    path('book_appointment/', book_appointment, name='book_appointment'),
    path('appointment_success/', appointment_success, name='appointment_success'),
    path('appointment_failure/', appointment_failure, name='appointment_failure'),
    path('checkout/<int:appointment_id>/', checkout, name='checkout'),
    path('consultant-details/<int:consultant_id>/', consultant_details, name='consultant_details'),
]
