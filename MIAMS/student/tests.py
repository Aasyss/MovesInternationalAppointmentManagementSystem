from django.test import TestCase, Client
from django.urls import reverse
from userregistration.models import UserProfile
from appointment_management.models import Setup_Availability

class StudentDashboardViewTest(TestCase):

    def setUp(self):
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

        # Create a test availability setup
        self.availability = Setup_Availability.objects.create(
            consultant=self.consultant,
            day='Monday',
            start_time='08:00:00',
            end_time='12:00:00'
        )

    def test_student_dashboard_view_GET(self):
        client = Client()
        response = client.get(reverse('student_dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student/student_dashboard.html')
        self.assertContains(response, 'Test Expertise')  # Make sure expertise is displayed

    def test_student_dashboard_view_with_expertise_GET(self):
        client = Client()
        response = client.get(reverse('student_dashboard') + '?expertise=Test Expertise')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student/student_dashboard.html')
        self.assertContains(response, 'Test Expertise')  # Make sure expertise is displayed
        self.assertContains(response, 'consultantuser')  # Make sure consultant is displayed

class ViewConsultantDetailsViewTest(TestCase):

    def setUp(self):
        # Create a test consultant user profile
        self.consultant = UserProfile.objects.create(
            user__username='consultantuser',
            expertise='Test Expertise',
            user__groups__name='consultant'
        )

        # Create a test availability setup
        self.availability = Setup_Availability.objects.create(
            consultant=self.consultant,
            day='Monday',
            start_time='08:00:00',
            end_time='12:00:00'
        )

    def test_view_consultant_details_view_GET(self):
        client = Client()
        response = client.get(reverse('view_consultant_details', args=[self.consultant.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student/view_consultant_details.html')
        self.assertContains(response, 'Test Expertise')  # Make sure expertise is displayed
        self.assertContains(response, 'Monday')  # Make sure availability is displayed
