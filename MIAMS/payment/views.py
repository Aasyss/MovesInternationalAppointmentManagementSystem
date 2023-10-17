#payment/view.py

from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from book_appointment.models import Appointment
from .models import Payment
from .forms import PaymentForm
import stripe
import json
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt # new
from datetime import datetime
from django.core.mail import send_mail
stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessView(TemplateView):
    template_name = 'payment/success.html'

@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLIC_KEY}
        return JsonResponse(stripe_config, safe=False)

def checkout(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    # Retrieve the amount from the appointment

    context = {
                'appointment': appointment,
               'appointment_id': appointment.id,
               }
    return render(request, 'payment/checkout.html', context)

def create_checkout_session(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    amount = int(appointment.amount * 100)
    product = stripe.Product.create(
        name='Payment for appointment with {}'.format(appointment.consultant.user.username),
        description = 'Powered by Moves International. Please submit the payment to confirm your appointment. Thank you.'
    )
    price = stripe.Price.create(
        product=product,
        unit_amount=amount,
        currency='aud',
    )
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancel/',
                # payment_link = payment_link,
                payment_method_types=['card'],
                # customer_details = {
                #     "email" : request.user.email,
                #     "name" : f"{request.user.first_name} {request.user.last_name}"
                # },
                customer_email = request.user.email,
                mode='payment',
                line_items=[
                    {
                        'price': price,
                        'quantity': 1,
                    }
                ]
            )
            payment = Payment(
                student=appointment.student,
                consultant=appointment.consultant,
                appointment=appointment,
                amount=appointment.amount,  # Use the amount from the appointment
                payment_status='paid'
            )
            payment.save()

            appointment.is_paid = True
            appointment.save()
            send_appointment_confirmation_email(appointment.id)
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


def send_appointment_confirmation_email(appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    amount = int(appointment.amount * 100)

    student = appointment.student.user
    consultant = appointment.consultant.user

    # Retrieve details
    student_email = student.email
    student_name = f"{student.first_name} {student.last_name}"

    consultant_email = consultant.email
    consultant_name = f"{consultant.first_name} {consultant.last_name}"


    # Render the HTML templates for the email content
    student_message = render_to_string('email/appointment_booked_student.html', {
        'date': appointment.appointment_datetime,
        'start_time': appointment.appointment_start_time.strftime('%Y-%m-%d %H:%M:%S'),
        'end_time': appointment.appointment_end_time.strftime('%Y-%m-%d %H:%M:%S'),
        'student_name': student_name,
        'consultant_name': consultant_name,
        'amount': amount
    })

    consultant_message = render_to_string('email/appointment_booked_consultant.html', {
        'date': appointment.appointment_datetime,
        'start_time': appointment.appointment_start_time.strftime('%Y-%m-%d %H:%M:%S'),
        'end_time': appointment.appointment_end_time.strftime('%Y-%m-%d %H:%M:%S'),
        'student_name': student_name,
        'consultant_name': consultant_name,
        'amount': amount
    })

    # Send email to student
    send_mail(
        'Appointment Booked',
        student_message,
        settings.HOST_EMAIL,
        [student_email],
        fail_silently=False,
        html_message=student_message
    )

    # Send email to consultant
    send_mail(
        'Appointment Booked',
        consultant_message,
        settings.HOST_EMAIL,
        [consultant_email],
        fail_silently=False,
        html_message=consultant_message
    )