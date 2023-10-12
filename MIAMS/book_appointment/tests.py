from django.test import TestCase, Client
from django.urls import reverse
from book_appointment.views import send_appointment_confirmation_email
from userregistration.models import User, UserProfile
from .models import Appointment
from appointment_management.models import Setup_Availability
from datetime import datetime, timedelta

class BookAppointmentViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.user_profile = UserProfile.objects.create(user=self.user, expertise='Test Expertise')
        self.consultant = UserProfile.objects.create(user=User.objects.create_user(username='consultant', password='password'))

        # Set up availability for the consultant
        now = datetime.now().time()
        availability = Setup_Availability.objects.create(
            consultant=self.consultant,
            monday_start_time=now,
            monday_end_time=(now + timedelta(hours=1))
        )

    def test_book_appointment_view_POST(self):
        self.client.login(username='testuser', password='password')

        response = self.client.post(reverse('book_appointment'), {
            'consultant': self.consultant.id,
            'date': datetime.now().date(),
            'appointment_start_time': (datetime.now().time() + timedelta(minutes=30)).strftime('%H:%M:%S'),
            'appointment_end_time': (datetime.now().time() + timedelta(hours=1, minutes=30)).strftime('%H:%M:%S')
        })

        self.assertEqual(response.status_code, 302)

        # Check if the appointment is created
        self.assertTrue(Appointment.objects.filter(
            student=self.user_profile,
            consultant=self.consultant,
            appointment_datetime__date=datetime.now().date()
        ).exists())

    def test_book_appointment_view_GET(self):
        self.client.login(username='testuser', password='password')

        response = self.client.get(reverse('book_appointment'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_appointment/book_appointment.html')

    def test_consultant_details_view(self):
        response = self.client.get(reverse('consultant_details', kwargs={'consultant_id': self.consultant.id}))

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            'first_name': self.consultant.user.first_name,
            'last_name': self.consultant.user.last_name,
            'email': self.consultant.user.email,
            'availabilities': []
        })

    def test_appointment_success_view(self):
        response = self.client.get(reverse('appointment_success'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_appointment/appointment_success.html')

    def test_appointment_failure_view(self):
        response = self.client.get(reverse('appointment_failure'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_appointment/appointment_failure.html')

    def test_send_appointment_confirmation_email(self):
        student_email = 'testuser@example.com'
        consultant_email = 'consultant@example.com'
        date = '2022-09-21'
        start_time = '09:00:00'
        end_time = '10:00:00'
        student_name = 'Test User'
        consultant_name = 'Test Consultant'

        send_appointment_confirmation_email(student_email, consultant_email, date, start_time, end_time, student_name, consultant_name)

        # Check if the emails were sent
        self.assertEqual(len(self.client.outbox), 2)
        self.assertEqual(self.client.outbox[0].subject, 'Appointment Booked')
        self.assertEqual(self.client.outbox[1].subject, 'Appointment Booked')
        self.assertIn(student_email, self.client.outbox[0].to)
        self.assertIn(consultant_email, self.client.outbox[1].to)
