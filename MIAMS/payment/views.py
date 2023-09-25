from django.shortcuts import render, get_object_or_404
from django.conf import settings
from .models import Appointment
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

def process_payment(request, appointment_id, amount):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    intent = stripe.PaymentIntent.create(
        amount=amount,
        currency='usd',
        payment_method_types=['card'],
    )
    client_secret = intent.client_secret

    return render(request, 'payment/payment.html', {'client_secret': client_secret, 'appointment': appointment})
