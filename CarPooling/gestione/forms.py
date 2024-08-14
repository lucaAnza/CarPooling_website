from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import *
from datetime import datetime , timedelta


class CreateVehicleForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "addcar_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("submit","Add vehicle"))
    
    # Improve form front-end
    last_inspection_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    # Makes "inspection_date" optional
    def __init__(self, *args, **kwargs):     
        super(CreateVehicleForm, self).__init__(*args, **kwargs)   
        self.fields['last_inspection_date'].required = False
        
    class Meta:
        model = Car
        fields = ["model", "license_plate", "km" , "last_inspection_date"]



class CreateTripForm(forms.Form):

    # User passed from the View
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', "None")
        super(CreateTripForm, self).__init__(*args, **kwargs)
        self.changeChoiche()

    # Set the list of possible car to use
    def changeChoiche(self):
        car_list = self.user.my_cars.all()
        car_choice = []
        for car in car_list:
            car_choice.append(  (f"{car.id}" , f"{car.model} [{car.license_plate}] - ❨{car.id}❩")  )
        self.fields["car"].choices = car_choice

    car_choice = None
    passenger_choice = [ ("1","1"), ("2","2") , ("3","3") , ("4","4") , ("5","5") , ("6","6") , ("7","7") ]

    # Ride
    car = forms.ChoiceField(label="Vehicle to use", required=True, choices=car_choice)
    departure_location = forms.CharField(label="Departure location",max_length=30, min_length=3, required=True)
    arrival_location = forms.CharField(label="Arrival   location",max_length=30, min_length=3, required=True)
    departure_time = forms.DateTimeField(
        initial=datetime.now().strftime("%Y-%m-%dT%H:%M"),
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
    )
    arrival_time = forms.DateTimeField(
        initial=datetime.now().strftime("%Y-%m-%dT%H:%M"),
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
    )

    # Booking
    open_registration_time = forms.DateTimeField(
        initial=datetime.now().strftime("%Y-%m-%dT%H:%M"),
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
    )
    close_registration_time = forms.DateTimeField(
        initial= (datetime.now()+timedelta(hours=5)).strftime("%Y-%m-%dT%H:%M"),
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
    )
    max_passenger = forms.ChoiceField(label="Max passengers", required=True, choices=passenger_choice)


class SearchTripForm(forms.Form):
    
    CHOICE_LIST = [("Destination","Search for destinations"), ("Departure","Search for departure") , ("Date","Search for Date")]
    search_where = forms.ChoiceField(label="Filter", required=True, choices=CHOICE_LIST)
    search_string = forms.CharField(label="Search String",max_length=100, min_length=3, required=True)
    
    