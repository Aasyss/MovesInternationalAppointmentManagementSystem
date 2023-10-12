from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from .models import UserProfile
from .forms import UserRegisterForm
from .views import CustomLoginView, redirect_after_login

class RegisterViewTest(TestCase):
    def test_register_view_GET(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_register_view_POST_student(self):
        response = self.client.post(reverse('register'), data={
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'role': 'student'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertTrue(User.objects.get(username='testuser').groups.filter(name='student').exists())

    def test_register_view_POST_consultant(self):
        response = self.client.post(reverse('register'), data={
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'role': 'consultant'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertTrue(User.objects.get(username='testuser').groups.filter(name='consultant').exists())

class ProfileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_profile_view_authenticated(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')

    def test_profile_view_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)  # Redirects to login page

class RedirectAfterLoginViewTest(TestCase):
    def test_redirect_after_login_consultant(self):
        consultant_group = Group.objects.create(name='consultant')
        self.user = User.objects.create_user(username='consultantuser', password='testpassword')
        self.user.groups.add(consultant_group)
        self.client.login(username='consultantuser', password='testpassword')
        response = self.client.get(reverse('redirect_after_login'))
        self.assertRedirects(response, reverse('dashboard'))

    def test_redirect_after_login_student(self):
        student_group = Group.objects.create(name='student')
        self.user = User.objects.create_user(username='studentuser', password='testpassword')
        self.user.groups.add(student_group)
        self.client.login(username='studentuser', password='testpassword')
        response = self.client.get(reverse('redirect_after_login'))
        self.assertRedirects(response, reverse('student_dashboard'))

    def test_redirect_after_login_other_user(self):
        self.user = User.objects.create_user(username='otheruser', password='testpassword')
        self.client.login(username='otheruser', password='testpassword')
        response = self.client.get(reverse('redirect_after_login'))
        self.assertRedirects(response, reverse('home'))

class ConsultantDetailsViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_consultant_details_view_GET(self):
        response = self.client.get(reverse('consultant_details'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/consultant_details.html')

    def test_consultant_details_view_POST_valid(self):
        response = self.client.post(reverse('consultant_details'), data={
            'field1': 'value1',  # Add valid form data here
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful submission
        # Add assertions for validating data in the database

    def test_consultant_details_view_POST_invalid(self):
        response = self.client.post(reverse('consultant_details'), data={
            'field1': '',  # Add invalid form data here
        })
        self.assertEqual(response.status_code, 200)  # Form submission failed, stays on the same page
        # Add assertions for error messages or form validation checks

class AddCertificateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_add_certificate_view_GET(self):
        response = self.client.get(reverse('add_certificate'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/add_certificate.html')

    def test_add_certificate_view_POST_valid(self):
        response = self.client.post(reverse('add_certificate'), data={
            'field1': 'value1',  # Add valid form data here
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful submission
        # Add assertions for validating data in the database

    def test_add_certificate_view_POST_invalid(self):
        response = self.client.post(reverse('add_certificate'), data={
            'field1': '',  # Add invalid form data here
        })
        self.assertEqual(response.status_code, 200)  # Form submission failed, stays on the same page
        # Add assertions for error messages or form validation checks

class AboutUsViewTest(TestCase):
    def test_about_us_view_GET(self):
        response = self.client.get(reverse('about_us'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/about_us.html')

class ContactUsViewTest(TestCase):
    def test_contact_us_view_GET(self):
        response = self.client.get(reverse('contact_us'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/contact_us.html')

class VisaApplicationViewTest(TestCase):
    def test_visa_application_view_GET(self):
        response = self.client.get(reverse('visa_application'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/visa_application.html')


