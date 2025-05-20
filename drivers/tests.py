from django.test import TestCase
from accounts.models import User
from drivers.models import DriverProfile

class DriverProfileSyncTest(TestCase):
    def test_driver_profile_creation_and_sync(self):
        user = User.objects.create_user(
            password="testpass",
            role="driver",
            cnic="12345-1234567-1",
            phone_number="03001234567",
            full_name="Test Driver",
            education="BSCS"
        )
        profile = DriverProfile.objects.get(user=user)
        self.assertEqual(profile.user.cnic, "12345-1234567-1")
        self.assertEqual(profile.user.full_name, "Test Driver")