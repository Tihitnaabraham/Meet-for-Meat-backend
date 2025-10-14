from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.models import User
from livestock.models import Livestock
from .models import KirchaGroup

class KirchaGroupTests(APITestCase):
    def setUp(self):
        self.organizer = User.objects.create_user(
            email="organizer@example.com",
            password="password123",
            user_type="organizer",
            phone_number="+1234567890",
            full_name="Organizer User"
        )
        self.member = User.objects.create_user(
            email="member@example.com",
            password="password123",
            user_type="member",
            phone_number="+1987654321",
            full_name="Member User"
        )
        self.invited_user = User.objects.create_user(
            email="invited@example.com",
            password="password123",
            user_type="member",
            phone_number="+1122334455",
            full_name="Invited User"
        )

        self.livestock = Livestock.objects.create(name='Test Livestock', description='Test livestock for testing')

        self.group = KirchaGroup.objects.create(
            organizer=self.organizer,
            livestock=self.livestock,
            group_type="Full Kircha",
            max_members=5,
            group_name="Test Group",
            slaughter_date="2025-11-10",
            slaughter_time="10:30:00",
            slaughter_method="self-slaughter",
            status="open",
            privacy="public"
        )
        self.client = APIClient()

    def test_create_kircha_group(self):
        self.client.force_authenticate(user=self.organizer)
        url = reverse('create_kircha_group')
        data = {
            "organizer": self.organizer.id,
            "livestock": self.livestock.id,
            "group_type": "Half Kircha",
            "max_members": 10,
            "group_name": "New Group",
            "slaughter_date": "2025-12-01",
            "slaughter_time": "08:00:00",
            "slaughter_method": "company-managed",
            "status": "open",
            "privacy": "private"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_join_group(self):
        self.client.force_authenticate(user=self.member)
        url = reverse('join_kircha_group')
        data = {
            "group": self.group.id,
            "member_full_name": "John Doe",
            "member_phone_number": "+1234567890",
            "member_delivery_address": "123 Farm Road",
            "payment_status": "pending",
            "group_id": self.group.id  # to satisfy permission class check
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invite_member(self):
        self.client.force_authenticate(user=self.organizer)
        url = reverse('invite_kircha_member')
        data = {
            "group": self.group.id,
            "invited_user": self.invited_user.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
