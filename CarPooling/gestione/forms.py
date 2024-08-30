from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.utils import timezone
from .models import *
from datetime import datetime , timedelta

from django.core.exceptions import ValidationError

class CreateVehicleForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "addcar_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("submit", "Add vehicle"))

    last_inspection_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super(CreateVehicleForm, self).__init__(*args, **kwargs)
        self.fields['last_inspection_date'].required = False

    class Meta:
        model = Car
        fields = ["model", "license_plate", "km", "last_inspection_date", "image"]



class CreateTripForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CreateTripForm, self).__init__(*args, **kwargs)
        self.change_choices()

    def change_choices(self):
        car_list = self.user.my_cars.all()
        car_choice = [(f"{car.id}", f"{car.model} [{car.license_plate}] - ❨{car.id}❩") for car in car_list]
        self.fields["car"].choices = car_choice

    car_choice = None
    passenger_choice = [("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"), ("6", "6"), ("7", "7")]

    car = forms.ChoiceField(label="Vehicle to use", required=True, choices=[])
    departure_location = forms.CharField(label="Departure location", max_length=30, min_length=3, required=True)
    arrival_location = forms.CharField(label="Arrival location", max_length=30, min_length=3, required=True)
    departure_time = forms.DateTimeField(
        initial=(datetime.now() + timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M"),
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
    )
    arrival_time = forms.DateTimeField(
        initial=(datetime.now() + timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M"),
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
    )
    open_registration_time = forms.DateTimeField(
        initial=(datetime.now() + timedelta(minutes=1)).strftime("%Y-%m-%dT%H:%M"),
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
    )
    close_registration_time = forms.DateTimeField(
        initial=(datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M"),
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
    )
    max_passenger = forms.ChoiceField(label="Max passengers", required=True, choices=passenger_choice)

    def clean_departure_time(self):
        departure_time = self.cleaned_data.get('departure_time')
        if departure_time is None or departure_time <= timezone.now():
            raise ValidationError("Departure time must be in the future.")
        return departure_time

    def clean_arrival_time(self):
        departure_time = self.cleaned_data.get('departure_time')
        arrival_time = self.cleaned_data.get('arrival_time')
        if departure_time is None:
            return arrival_time
        elif arrival_time is None or arrival_time <= departure_time:
            raise ValidationError("Arrival time must be after the departure time.")
        return arrival_time

    def clean_max_passenger(self):
        max_passenger = self.cleaned_data.get('max_passenger')
        if max_passenger is None or int(max_passenger) <= 0:
            raise ValidationError("Max passenger must be greater than 0.")
        return max_passenger

    def clean_car(self):
        car_id = self.cleaned_data.get('car')
        if car_id is None:
            raise ValidationError("Car selection is required.")
        try:
            car = Car.objects.get(id=car_id, user=self.user)
        except Car.DoesNotExist:
            raise ValidationError("You must own the selected car.")
        return car

    def clean(self):
        cleaned_data = super().clean()
        departure_time = cleaned_data.get('departure_time')
        arrival_time = cleaned_data.get('arrival_time')
        open_registration_time = cleaned_data.get('open_registration_time')
        close_registration_time = cleaned_data.get('close_registration_time')
        car = cleaned_data.get('car')

        if departure_time is None or arrival_time is None or open_registration_time is None or close_registration_time is None:
            return  # Skip validation if any of these fields are None

        if open_registration_time >= departure_time:
            self.add_error('open_registration_time', "Open registration time must be before departure time.")

        if close_registration_time >= departure_time or close_registration_time <= open_registration_time:
            self.add_error('close_registration_time', "Close registration time must be after open registration time and before departure time.")

        if car and Ride.objects.filter(
                car=car,
                departure_time__lt=arrival_time,
                arrival_time__gt=departure_time
        ).exists():
            self.add_error('car', "The selected car is already booked for the chosen time period.")

        return cleaned_data

class SearchTripForm(forms.Form):

    choice_list = [("Destination","Search for destinations"), ("Departure","Search for departure") ]
    search_where = forms.ChoiceField(label="Filter", required=True, choices=choice_list)
    search_string = forms.CharField(label="Search String",max_length=100, min_length=3, required=True)

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ["model", "license_plate", "km", "last_inspection_date", "image"]

    # Customize the widget for `last_inspection_date`
    last_inspection_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date', 'class': 'form-control'})
    )
    
class CreateReviewForm(forms.ModelForm):

    RATING_CHOICES = [
        (1, '1 - Poor ⭐'),
        (2, '2 - Fair ⭐⭐'),
        (3, '3 - Good ⭐⭐⭐'),
        (4, '4 - Very Good ⭐⭐⭐⭐'),
        (5, '5 - Excellent ⭐⭐⭐⭐⭐'),
    ]

    rating = forms.ChoiceField(choices=RATING_CHOICES)

    comment = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Enter your comments here (Max 100 character) ',
            'class': 'form-control'
        })
    )

    class Meta:
        model = Review
        fields = ["rating", "comment"]