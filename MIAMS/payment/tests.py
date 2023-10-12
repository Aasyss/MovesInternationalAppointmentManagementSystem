from django.test import TestCase, Client
from django.urls import reverse
from userregistration.models import UserProfile
from book_appointment.models import Appointment
from .models import Payment
import stripe
from django.conf import settings
from datetime import datetime
from django.core import mail

stripe.api_key = settings.STRIPE_SECRET_KEY

class CheckoutViewTest(TestCase):

    def setUp(self):
        self.client = Client()

        # Create a test user profile
        self.user_profile = UserProfile.objects.create(
            user__username='testuser',
            expertise='Test Expertise'
        )

        # Create a test consultant user profile
        self.consultant = UserProfile.objects.create(
            user__username='consultantuser',
            expertise='Test Expertise',
            user__groups__name='consultant'
        )

        # Create a test appointment
        self.appointment = Appointment.objects.create(
            student=self.user_profile,
            consultant=self.consultant,
            appointment_datetime=datetime.now(),
            appointment_start_time=datetime.now(),
            appointment_end_time=datetime.now(),
            amount=100
        )

    def test_checkout_view_GET(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('checkout', args=[self.appointment.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'payment/checkout.html')
        self.assertContains(response, 'Payment for appointment with consultantuser')  # Make sure consultant name is displayed

    def test_create_checkout_session_view_GET(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('create_checkout_session', args=[self.appointment.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTrue('sessionId' in response.json())

    def test_send_appointment_confirmation_email(self):
        send_appointment_confirmation_email(self.appointment.id)
        
        # Check if two emails are sent
        self.assertEqual(len(mail.outbox), 2)

        # Check email subject and body content
        self.assertEqual(mail.outbox[0].subject, 'Appointment Booked')
        self.assertIn('Appointment Booked', mail.outbox[0].body)
        self.assertIn('testuser', mail.outbox[0].body)
        self.assertIn('consultantuser', mail.outbox[0].body)
