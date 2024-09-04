import os
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import datetime

class Car(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True , related_name="my_cars")
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
            out = str(out) + f' [👤🗑] {self.model} ({self.license_plate}) - {self.km} Km \n\tLast inspection : {str(self.last_inspection_date)} \n'
        elif(self.user != None):
            out = str(out) + f'  [{self.user.username}] {self.model} ({self.license_plate}) - {self.km} Km \n'
        else:
            out = str(out) + f' [👤🗑] {self.model} ({self.license_plate}) - {self.km} Km \n'

        return out

    def clean(self):
        if self.km < 0:
            raise ValidationError('Kilometers cannot be negative.')

    def save(self, *args, **kwargs):
        self.full_clean()  
        super(Car, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Cars"


class Review(models.Model):
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    comment = models.CharField(max_length = 100)

    def __str__(self):
        return f'Review {self.id}: Rating {self.rating} - Comment: {self.comment}'

    def save(self, *args, **kwargs):
        self.full_clean()  # Make validation of rating
        super().save(*args, **kwargs)

class Ride(models.Model):
    car = models.ForeignKey(Car , on_delete=models.CASCADE , default = None ,null=False , related_name="my_rides")
    user = models.ForeignKey(User, on_delete=models.PROTECT,blank=True,null=True,default=None, related_name="my_rides")
    departure_location = models.CharField(max_length=30 , null  = False , default = "NO_LOCATION_D")
    departure_state = models.CharField(max_length=30 , null  = False , default = "NO_STATE_D")
    departure_address = models.CharField(max_length=30 , null  = False , default = "NO_ADDRESS_D")
    arrival_location = models.CharField(max_length=30 , null = False , default = "NO_LOCATION_A")
    arrival_state = models.CharField(max_length=30 , null  = False , default = "NO_STATE_A")
    arrival_address = models.CharField(max_length=30 , null  = False , default = "NO_ADDRESS_A")
    departure_time = models.DateTimeField(null=False , default=timezone.make_aware(timezone.datetime(1970, 1, 1, 0, 0, 0)))
    arrival_time = models.DateTimeField(null=False , default=timezone.make_aware(timezone.datetime(1970, 1, 1, 0, 0, 0)))
    open_registration_time = models.DateTimeField(null = False , default=timezone.make_aware(timezone.datetime(1970, 1, 1, 0, 0, 0)))
    close_registration_time = models.DateTimeField(null = False , default=timezone.make_aware(timezone.datetime(1970, 1, 1, 0, 0, 0)))
    max_passenger = models.IntegerField(default=0 , null = False )
    image = models.ImageField(upload_to='ride_images/', null=True, blank=True)

    #TODO: aggiungere campi mancanti
    def __str__(self):
        if self.image != None : 
            return f'Ride : {self.id} - Departure: {self.departure_state} , {self.departure_location} ,  {self.departure_address} - Arrival: {self.arrival_state} , {self.arrival_location} , {self.arrival_address} - Trip : ({self.departure_time} to {self.arrival_time} ) - Booking : ({self.open_registration_time} to {self.close_registration_time} ) - IMG : {self.image}'
        else:
            return f'Ride : {self.id} - Departure: {self.departure_state} , {self.departure_location} ,  {self.departure_address} - Arrival: {self.arrival_state} , {self.arrival_location} , {self.arrival_address} - Trip : ({self.departure_time} to {self.arrival_time} ) - Booking : ({self.open_registration_time} to {self.close_registration_time} ) '
    
    def delete(self, *args, **kwargs):
        #Before the deletion of the element, the image must be deleted in the directory
        if self.image:
            image_path = os.path.join(settings.MEDIA_ROOT, self.image.name)
            if os.path.isfile(image_path):
                os.remove(image_path)
        super(Ride, self).delete(*args, **kwargs)
    
    def is_running(self):
        current_time = timezone.now()
        if(current_time >= self.departure_time and current_time <= self.arrival_time):
            return True
        else:
            return False
        
    def get_count_passenger(self):
        return int(len(Passenger.objects.filter(ride = self.id)))
         
    def clean(self):
        if self.departure_time > self.arrival_time:
            raise ValidationError('Arrival time cannot be before the Departure time')
        if self.open_registration_time > self.close_registration_time:
            raise ValidationError("Close registration cannot be before the Open registration time")

    def save(self, *args, **kwargs):
        self.full_clean()  # Call validations
        super().save(*args, **kwargs)
    
class Passenger(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE , related_name = "passengers")
    user = models.ForeignKey(User, on_delete=models.CASCADE , related_name = "passengers_ride" )
    review_id = models.ForeignKey(Review, on_delete=models.CASCADE , null = True , default = None , blank = True)

    # Primary Key (ride,user)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['ride', 'user'], name='passenger_primary_key') # Composite Key
        ]
    def __str__(self):
        if self.review_id != None : 
            return f'Passenger [ID={self.id}] : (User-{self.user.id} , Ride {self.ride.id}) ---> Review {self.review_id.id}'
        else:
            return f'Passenger [ID={self.id}] : (User-{self.user.id} , Ride {self.ride.id})'

    def clean(self):
        count = int(self.ride.get_count_passenger())
        # Condition is == because we are testing before the Passenger is created
        if count == self.ride.max_passenger:
            raise ValidationError(f"A Ride cannot has [passenger > max_passenger] ({count} / {self.ride.max_passenger})")

    def save(self, *args, **kwargs):
        self.full_clean()  # Call validations
        super().save(*args, **kwargs)

    

            
            
