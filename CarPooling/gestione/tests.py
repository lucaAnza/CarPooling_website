from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Car, Ride, Passenger, Review
import os
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError


class RideModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        
        # Create a Car test
        self.car = Car.objects.create(
            user=self.user,
            model='Test Model',
            license_plate='ABC123',
            km=10000,
            last_inspection_date=timezone.now().date(),
            image=None
        )

        
        

        # Create a Ride test
        self.ride = Ride.objects.create(
            car=self.car,
            user=self.user,
            departure_location='Start City',
            arrival_location='End City',
            departure_time=timezone.now() + timezone.timedelta(hours=1),
            arrival_time=timezone.now() + timezone.timedelta(hours=3),
            open_registration_time=timezone.now() - timezone.timedelta(days=1),
            close_registration_time=timezone.now() + timezone.timedelta(hours=0.5),
            max_passenger=4,
            image=None
        )

    def test_ride_creation(self):
        self.assertEqual(self.ride.departure_location, 'Start City')
        self.assertEqual(self.ride.arrival_location, 'End City')
        self.assertEqual(self.ride.max_passenger, 4)
        self.assertFalse(self.ride.is_running())

    def test_ride_str(self):
        self.assertEqual(
            str(self.ride),
            f'Ride {self.ride.id} - Departure: Start City - Arrival: End City - Departure Time: {self.ride.departure_time} - Arrival Time: {self.ride.arrival_time}'
        )

    def test_ride_is_running(self):
        self.ride.departure_time = timezone.now() - timezone.timedelta(minutes=30)
        self.ride.arrival_time = timezone.now() + timezone.timedelta(minutes=30)
        self.assertTrue(self.ride.is_running())

    def test_ride_image_deletion(self):
        
        #Load a fake img
        self.ride.image = SimpleUploadedFile(name='test_image.jpg', content=b'Test image content', content_type='image/jpeg')
        self.ride.save()
        image_path = self.ride.image.path
        
        # Check if the fake img exist
        self.assertTrue(os.path.isfile(image_path))

        # Delete img and check if it is removed
        self.ride.delete()
        self.assertFalse(os.path.isfile(image_path))

    def test_km_cannot_be_negative(self):
        
        self.assertRaises(
			ValidationError,
			# Create a Car test (km<0)
            Car.objects.create,
            user=self.user,
            model='Test Model',
            license_plate='ABC456',
            km=-100,
            last_inspection_date=timezone.now().date(),
            image=None)
		
