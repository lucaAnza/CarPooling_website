import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Car(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT,blank=True,null=True , related_name="my_cars")
    model = models.CharField(max_length=50)
    license_plate = models.CharField(max_length=15)
    km = models.IntegerField(default=0)
    last_inspection_date = models.DateField(default=None , null = True , blank=True)
    image = models.ImageField(upload_to='car_images/', null=True, blank=True)

    def delete(self, *args, **kwargs):
        #Before the deletion of the element, the image must be deleted in the directory
        if self.image:
            image_path = os.path.join(settings.MEDIA_ROOT, self.image.name)
            if os.path.isfile(image_path):
                os.remove(image_path)
        super(Car, self).delete(*args, **kwargs)
    def __str__(self):
        out = "{" + str(self.id) + "}"  # Primary key
        if(self.user != None and self.last_inspection_date != None) :
            out = str(out) +  f'  [{self.user.username}] {self.model} ({self.license_plate}) - {self.km} Km\n\tLast inspection : {str(self.last_inspection_date)} \n'
        elif(self.last_inspection_date != None) :
            out = str(out) + f' {self.model} ({self.license_plate}) - {self.km} Km \n\tLast inspection : {str(self.last_inspection_date)} \n'
        elif(self.user != None):
            out = str(out) + f'  [{self.user.username}] {self.model} ({self.license_plate}) - {self.km} Km \n'
        else:
            out = str(out) + f' {self.model} ({self.license_plate}) - {self.km} Km \n'

        return out

    class Meta:
        verbose_name_plural = "Cars"


class Review(models.Model):
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    comment = models.CharField(max_length = 100)

    def __str__(self):
        return f'Review {self.id}: Rating {self.rating} - Comment: {self.comment}'

class Ride(models.Model):
    car = models.ForeignKey(Car , on_delete=models.CASCADE , default = None ,null=False , related_name="my_rides")
    user = models.ForeignKey(User, on_delete=models.PROTECT,blank=True,null=True,default=None, related_name="my_rides")
    departure_location = models.CharField(max_length=30 , null  = False)
    arrival_location = models.CharField(max_length=30 , null = False)
    departure_time = models.DateTimeField(null=False)
    arrival_time = models.DateTimeField(null=False)
    open_registration_time = models.DateTimeField(null = False)
    close_registration_time = models.DateTimeField(null = False)
    max_passenger = models.IntegerField(default=0 , null = False)

    #TODO: aggiungere campi mancanti
    def __str__(self):
        return f'Ride {self.id} - Departure: {self.departure_location} - Arrival: {self.arrival_location} - Departure Time: {self.departure_time} - Arrival Time: {self.arrival_time}'

class Passenger(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE , related_name = "passengers")
    user = models.ForeignKey(User, on_delete=models.CASCADE , related_name = "passengers_ride" )
    review_id = models.ForeignKey(Review, on_delete=models.CASCADE , null = True , default = None)

    # Primary Key (ride,user)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['ride', 'user'], name='passenger_primary_key') # Composite Key
        ]
    def __str__(self):
        return f'Passenger [ID={self.id}] : (User-{self.user.id} , Ride {self.ride.id}) ---> Review {self.review_id.id}'
