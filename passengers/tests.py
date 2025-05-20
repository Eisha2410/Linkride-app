from django.test import TestCase
from accounts.models import User
from passengers.models import PassengerProfile

class PassengerProfileSyncTest(TestCase):
    def test_passenger_profile_creation_and_sync(self):
        user = User.objects.create_user(
            password="testpass",
            role="passenger",
            cnic="12345-1234567-1",
            phone_number="03001234567",
            full_name="Test passenger",
            education="BSCS"
        )
        profile = PassengerProfile.objects.get(user=user)
        self.assertEqual(profile.user.cnic, "12345-1234567-1")
        self.assertEqual(profile.user.full_name, "Test passenger")

