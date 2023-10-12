from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from .models import UserProfile, Setup_Availability
from .forms import AvailabilityForm

class SetAvailabilityViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = UserProfile.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_set_availability_view_GET(self):
        response = self.client.get(reverse('set_availability'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointment_management/set_availability.html')
        self.assertIsInstance(response.context['form'], AvailabilityForm)

    def test_set_availability_view_POST_valid_form(self):
        start_date = timezone.now().date()  # Assuming availability starts from today
        form_data = {
            'start_date': start_date,
            'monday_start_time': '09:00',
            'monday_end_time': '17:00',
            'tuesday_start_time': '09:00',
            'tuesday_end_time': '17:00',
            'wednesday_start_time': '09:00',
            'wednesday_end_time': '17:00',
            'thursday_start_time': '09:00',
            'thursday_end_time': '17:00',
            'friday_start_time': '09:00',
            'friday_end_time': '17:00',
            'saturday_start_time': '09:00',
            'saturday_end_time': '17:00',
            'sunday_start_time': '09:00',
            'sunday_end_time': '17:00',
        }

        response = self.client.post(reverse('set_availability'), data=form_data)

        self.assertEqual(response.status_code, 302)

        # Check if the availability data is saved
        availability = Setup_Availability.objects.get(consultant=self.user)
        self.assertEqual(availability.start_date, start_date)
        self.assertEqual(availability.monday_start_time.strftime('%H:%M'), '09:00')
        self.assertEqual(availability.monday_end_time.strftime('%H:%M'), '17:00')
        self.assertEqual(availability.tuesday_start_time.strftime('%H:%M'), '09:00')
        self.assertEqual(availability.tuesday_end_time.strftime('%H:%M'), '17:00')
        self.assertEqual(availability.wednesday_start_time.strftime('%H:%M'), '09:00')
        self.assertEqual(availability.wednesday_end_time.strftime('%H:%M'), '17:00')
        self.assertEqual(availability.thursday_start_time.strftime('%H:%M'), '09:00')
        self.assertEqual(availability.thursday_end_time.strftime('%H:%M'), '17:00')
        self.assertEqual(availability.friday_start_time.strftime('%H:%M'), '09:00')
        self.assertEqual(availability.friday_end_time.strftime('%H:%M'), '17:00')
        self.assertEqual(availability.saturday_start_time.strftime('%H:%M'), '09:00')
        self.assertEqual(availability.saturday_end_time.strftime('%H:%M'), '17:00')
        self.assertEqual(availability.sunday_start_time.strftime('%H:%M'), '09:00')
        self.assertEqual(availability.sunday_end_time.strftime('%H:%M'), '17:00')

    def test_set_availability_view_POST_invalid_form(self):
        # Missing required form fields
        form_data = {
            'start_date': timezone.now().date(),
            # Omitted other fields
        }

        response = self.client.post(reverse('set_availability'), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointment_management/set_availability.html')
        self.assertIsInstance(response.context['form'], AvailabilityForm)

        # Check if form errors are displayed
        self.assertIn('This field is required.', str(response.content))

    def test_set_availability_view_POST_exception(self):
        # Simulate an exception during form saving
        form_data = {
            'start_date': timezone.now().date(),
            'monday_start_time': '09:00',
            'monday_end_time': '17:00',
            'tuesday_start_time': '09:00',
            'tuesday_end_time': '17:00',
            'wednesday_start_time': '09:00',
            'wednesday_end_time': '17:00',
            'thursday_start_time': '09:00',
            'thursday_end_time': '17:00',
            'friday_start_time': '09:00',
            'friday_end_time': '17:00',
            'saturday_start_time': '09:00',
            'saturday_end_time': '17:00',
            'sunday_start_time': '09:00',
            'sunday_end_time': '17:00',
        }

        with self.assertRaises(Exception):
            response = self.client.post(reverse('set_availability'), data=form_data)

            # Check if an error message is printed
            self.assertIn('Error saving availability data:', str(response.content))

class DashboardViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = UserProfile.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_dashboard_view(self):
        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointment_management/dashboard.html')
