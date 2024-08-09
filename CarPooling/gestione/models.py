from django.db import models
from django.contrib.auth.models import User

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
    