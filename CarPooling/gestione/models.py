from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Car(models.Model):
    model = models.CharField(max_length=50)
    license_plate = models.CharField(max_length=15)
    km = models.IntegerField(default=-1)
    last_inspection_date = models.DateField(default=None)
    
    def __str__(self):
        out = f'{self.model} ({self.license_plate}) - {self.km} Km\n\tLast inspection : {str(self.last_inspection_date)}'
        return out

    class Meta:
        verbose_name_plural = "Cars"


class Booking(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT,blank=True,null=True,default=None, related_name="booking_creator")
    car = models.ForeignKey(Car , on_delete=models.CASCADE)
    open_registration_time = models.DateField(default=None)
    close_registration_time = models.DateField(default=None)
    max_passenger = models.IntegerField(default=0)
    
    def __str__(self):
        return f'Booking {self.id}: User {self.user_id.id} - Car {self.car.id} - Open: {self.open_registration_time} - Close: {self.close_registration_time} - Max passengers: {self.max_passenger}'

class Review(models.Model):
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    comment = models.CharField(max_length = 100)

    def __str__(self):
        return f'Review {self.id}: Rating {self.rating} - Comment: {self.comment}'

class Ride(models.Model):
    departure_location = models.CharField(max_length=15)
    arrival_location = models.CharField(max_length=15)
    departure_time = models.DateField(null=False)
    arrival_time = models.DateField(null=False)
    max_passenger = models.IntegerField(default=0)

    def __str__(self):
        return f'Ride {self.id}: Passenger {self.passenger_id.id} - Departure: {self.departure_location} - Arrival: {self.arrival_location} - Departure Time: {self.departure_time} - Arrival Time: {self.arrival_time} - Max passengers: {self.max_passenger}'

class Passenger(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_id = models.ForeignKey(Review, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['ride', 'user'], name='unique_ride_user') # Composite Key
        ]
    def __str__(self):
        return f'Passenger {self.id}: User {self.user.id} - Ride {self.ride.id} - Review {self.review_id.id}'











    


