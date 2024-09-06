from gestione.models import Car,Ride
from django.contrib.auth.models import User , Group
from django.utils import timezone
from datetime import datetime,timedelta
import random
import time

def erase_car_tables():
    print("\nDeleting Car table DB 🗑️ \n")
    Car.objects.all().delete()

def func_time(off_year=None, off_month=None, off_day=None):
        if off_year == 0 and off_month==0 and off_day==0:
            return None
        tz = timezone.now()
        out = datetime(tz.year-off_year,tz.month-off_month,
                    tz.day-off_day,tz.hour,tz.minute, tz.second)
        return out 


def init_db():

    if len(Car.objects.all()) != 0:
        return

    cardict = {
        "model" : ["Ford", "Model2", "Model3", "Model4", "Model5"],
        "license_plate" : ["AB123CD", "EF456GH", "IJ789KL", "MN012OP", "QR345ST"],
        "km" : [200000 , 150000, 43414, 1012, 4000000],
        "last_inspection_date" : [[ func_time(y,m,d) for y in range(2) for m in range(2) for d in range(2) ]]
    }

    for i in range(5):
        c = Car()
        for k in cardict:
            if k == "model":
                    c.model = cardict[k][i]
            if k == "license_plate":
                    c.license_plate = cardict[k][i]
            if k == "km":
                    c.km = cardict[k][i]
            if k == "last_inspection_date":
                    c.last_inspection_date = datetime.now()
        try:
            admin_user = User.objects.get(username='admin') # Try to get the user with username 'admin'
        except User.DoesNotExist:
            print("Errore - USERNAME admin doesn't exist! (initcmds.py) ")
            admin_user = None # Handle the case where the user does not exist
        c.user_id = admin_user
        c.save()

    print("DUMP DB")
    print(Car.objects.all()) 


def func_time(year_offset=0, month_offset=0, day=0, hour=0, minute=0):
    """Helper function to get a time with specific offsets."""
    tz = timezone.now()
    return timezone.make_aware(datetime(
        tz.year + year_offset,
        tz.month + month_offset,
        day,
        hour, minute))

def generate_next_month_rides( ride_to_generate = 10):
    
    # If is true block the creation process
    locked = True

    if len(Ride.objects.all()) != 0 and locked:
        print("\nRide table is already populated.")
        print("Please comment the function [generate_next_month_rides()] on Carpooling/urls.py \n")
        return

    string = input("Danger : you are generating " + str(ride_to_generate) + " rides are you sure ? \n - Write 'YES' if you confirmed : ")

    if(string != 'YES'):
        print("Operation suppressed \n\n")
        return

    users = User.objects.all()  # Retrieve all users in the system
    cars = Car.objects.all()    # Retrieve all cars in the system
    
    if not users.exists() or not cars.exists():
        print("Error: there aren't car or user in the system!")
        return

    days = list(range(1, 28))  
    
    ride_data = {
        "departure_location": ["Roma", "Milano", "Torino", "Napoli", "Firenze"],
        "departure_address": ["Via Carducci", "Via Dante Alighieri", "Via Sallo", "Via Marconi", "Via Napoleone"],
        "arrival_location": ["Bologna", "Venice", "Palermo", "Genoa", "Catania"],
        "arrival_address": ["Via Garibaldi", "Via Cavour", "Corso Italia", "Via XX Settembre", "Via Mazzini"],
        "max_passenger": [1 , 2, 3, 4, 5, 6]
    }

    driver_group = Group.objects.get(name = "Driver").id
    users = User.objects.filter(groups= driver_group)  # Retrieve only driver users

    for i in range(ride_to_generate):
        print("Generating car(", i , ")...")
        ride = Ride()

         # Get the 'Driver' group
        try:
            driver_group = Group.objects.get(name='Driver')
        except Group.DoesNotExist:
            print("Errore: Il gruppo 'Driver' non esiste.")
            return

        # Get users in the 'Driver' group
        ride.user = random.choice(users) # Choose a user from all drivers
        cars = Car.objects.filter(user = ride.user)  # Retrieve all cars of the user
        ride.car = random.choice(cars) # Choose a car from the user's car

        # Randomly assign locations and details
        ride.departure_location = random.choice(ride_data["departure_location"])
        ride.departure_state = "Italy"
        ride.departure_address = random.choice(ride_data["departure_address"])
        ride.arrival_location = random.choice(ride_data["arrival_location"])
        ride.arrival_state = "Italy"
        ride.arrival_address = random.choice(ride_data["arrival_address"])
        ride.max_passenger = random.choice(ride_data["max_passenger"])
        ride.image = None
    
        # Generate departure and arrival times 
        random_day = random.choice(days)
        ride.departure_time = func_time(0, 1, random_day, random.randint(6, 10), random.randint(0, 59))
        ride.arrival_time = ride.departure_time + timedelta(hours=random.randint(1, 5))

        # Booking times
        ride.open_registration_time = timezone.now()
        ride.close_registration_time = ride.departure_time - timedelta(hours= 4)
        ride.save()

    print(f"Successfully created {ride_to_generate} rides\n\n")