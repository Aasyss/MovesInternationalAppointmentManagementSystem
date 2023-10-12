from django.test import TestCase, Client
from django.urls import reverse
from userregistration.models import User, UserProfile
from .models import Room

class CreateRoomViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_create_room_view_POST(self):
        user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        response = self.client.post(reverse('create_room', args=['some-uuid']), {'name': 'Test Name', 'url': 'http://example.com'})

        self.assertEqual(response.status_code, 200)

        # Check if the room is created
        self.assertTrue(Room.objects.filter(uuid='some-uuid', client='Test Name', url='http://example.com').exists())

class AdminViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_admin_view_GET(self):
        user = User.objects.create_user(username='adminuser', password='password', is_staff=True)
        self.client.login(username='adminuser', password='password')

        response = self.client.get(reverse('admin'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'live_chat/admin.html')

class RoomViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_room_view_GET(self):
        room = Room.objects.create(uuid='some-uuid', client='Test Name', url='http://example.com')

        response = self.client.get(reverse('room', args=['some-uuid']))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'live_chat/room.html')
        self.assertEqual(response.context['room'], room)

class DeleteRoomViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_delete_room_view_GET(self):
        user = User.objects.create_user(username='adminuser', password='password', is_staff=True)
        self.client.login(username='adminuser', password='password')
        room = Room.objects.create(uuid='some-uuid', client='Test Name', url='http://example.com')

        response = self.client.get(reverse('delete_room', args=['some-uuid']))

        self.assertEqual(response.status_code, 302)

        # Check if the room is deleted
        self.assertFalse(Room.objects.filter(uuid='some-uuid').exists())
