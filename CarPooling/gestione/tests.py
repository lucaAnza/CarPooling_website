from django.test import TestCase , Client
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Car, Ride, Passenger, Review 
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
import os




# Test on Model(Ride)
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
		

# Test on FBV (show_review)
class ShowReviewViewTest(TestCase):
    
    def setUp(self):
        # Setup initial data
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user2 = User.objects.create_user(username='testuser2', password='testpassword')
        self.user3 = User.objects.create_user(username='testuser3', password='testpassword')
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

        # Create a Car test
        self.car = Car.objects.create(
            user=self.user,
            model='Test Model',
            license_plate='ABC123',
            km=10000,
            last_inspection_date=timezone.now().date(),
            image=None
        )
        # Ride + Review test
        self.ride = Ride.objects.create(car = self.car , user = self.user)
        self.review1 = Review.objects.create(rating=4, comment="Good ride")
        self.review2 = Review.objects.create(rating=5, comment="Excellent ride")
        # Passengers test
        self.passenger1 = Passenger.objects.create(ride=self.ride, review_id=self.review1 , user = self.user2)
        self.passenger2 = Passenger.objects.create(ride=self.ride, review_id=self.review2 , user = self.user3)
    
    def test_show_review_view(self):
        response = self.client.get(reverse('review', args=[self.ride.id]))
        
        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that the context contains the correct ride ID
        self.assertEqual(response.context['ride_id'], self.ride.id)

        # Check that the context contains the correct number of reviews
        self.assertEqual(len(response.context['object_list']), 2)

        # Check that the context contains the correct rating sum (average rating)
        self.assertEqual(response.context['rating_sum'], 4)  # (4+5)/2 = 4

        # Check that the template used is correct
        self.assertTemplateUsed(response, 'reviews.html')

    def test_show_review_view_no_reviews(self):
        
        # Test the case where there are no reviews for the ride
        self.passenger1.delete()
        self.passenger2.delete()

        response = self.client.get(reverse('review', args=[self.ride.id]))
        
        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that the context contains the correct ride ID
        self.assertEqual(response.context['ride_id'], self.ride.id)

        # Check that the context contains an empty object list
        self.assertEqual(len(response.context['object_list']), 0)

        # Check that the rating sum is not calculated and handled correctly
        self.assertEqual(response.context.get('rating_sum') , 0)

    def test_show_review_view_no_reviews_with_reviews(self):
        # Test the case where passengers exist, but none have reviews
        self.passenger1.review_id = None
        self.passenger1.save()
        self.passenger2.review_id = None
        self.passenger2.save()

        response = self.client.get(reverse('review', args=[self.ride.id]))

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that the context contains the correct ride ID
        self.assertEqual(response.context['ride_id'], self.ride.id)

        # Check that the context contains an empty object list
        self.assertEqual(len(response.context['object_list']), 0)

        # Check that the rating sum is not calculated and handled correctly
        self.assertEqual(response.context.get('rating_sum') , 0)

    def test_show_review_view_not_logged_in(self):
        # Test that the view redirects to login if the user is not logged in
        self.client.logout()
        response = self.client.get(reverse('review', args=[self.ride.id]) , follow = True)
        
        # Check for redirect to login page
        self.assertRedirects(response, f'/login/?login=needed&next=/gestione/review/{self.ride.id}')
    
    def test_forbidden_rating(self):

        self.assertRaises(
			ValidationError,
			# Create a Rating forbidden
            Review.objects.create,
            rating = 6,
            comment = 'i am trying to cheat'
            )
        
        #Check the content of the passenger1
        self.passenger1.review_id = self.review1

        

        
        