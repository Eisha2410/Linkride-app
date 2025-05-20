from django.test import TestCase
from accounts.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

from drivers.models import DriverProfile, Vehicle  # adjust import as needed

class RideCreationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            cnic="1234567890123",
            phone_number="03001234567",
            password="testpass",
        )

        # Optional: create vehicle first if needed, else skip vehicle field
        vehicle = Vehicle.objects.create(
            driver=self.user,
            model="Test Car",
            model_year=2020,
            vehicle_color="Black",
            vehicle_number="XYZ123"
        )

        # Create DriverProfile for the user, linked to the vehicle
        DriverProfile.objects.create(
            user=self.user,
            cnic="1234567890123",
            phone_number="03001234567",
            full_name="Test Driver",
            education="BSCS",
            vehicle_number="XYZ123",
            license_number="LIC123456",
            experience_years=3,
            vehicle=vehicle
        )

        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_ride(self):
        data = {
            "origin": "City A",
            "destination": "City B",
            # include any required fields your ride creation expects
        }
        response = self.client.post("/api/rides/", data)
        self.assertEqual(response.status_code, 201)
