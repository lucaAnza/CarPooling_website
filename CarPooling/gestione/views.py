from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
from django.utils import timezone
from django.shortcuts import get_object_or_404 , render , redirect
from django.urls import reverse,reverse_lazy
#Models
from .models import *
from .forms import *
from django.contrib.auth.models import User

#CBV
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView

#Authentication
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin # pipenv install django-braces
from django.contrib.auth.decorators import user_passes_test


def home_page(request):

    response = "Hi i am luke!"

    return HttpResponse(response)

def elenca_params(request):
    response = ""
    
    for k in request.GET:
        response += request.GET[k] + " "

    return HttpResponse(response)

def two_params(request , nome , eta):
    response = nome + " " + str(eta)
    return HttpResponse(response)

def hello_template(request):
    ctx= { "title" : "Hello Template",
           "lista" : [datetime.now() , datetime.today().strftime('%A') , datetime.today().strftime('%B')]}
    return render(request, template_name = 'base_extended.html' , context = ctx)

def play_with_database(request):

    templ = "play_with_database.html"


    # Get element example
    ctx = { "title":"Lista di Macchine", "carlist": Car.objects.all()}

    # Filtering Example
    km_threshold = 10000
    lista_filtrata = Car.objects.filter(km__gte=km_threshold)
    lista_filtrata = Car.objects.exclude(km__lt=km_threshold)
    lista_filtrata = Car.objects.filter(model="Ford") #Case insensitive
    # for l in Car.objects.raw("SELECT * FROM gestione_car WHERE km >= %s", [km_threshold]):  ## RAW QUERY

    # Add entry
    """c = Car()
    c.model = "Mustang"
    c.license_plate = "NY244DC"
    c.km = 3002
    c.last_inspection_date = timezone.now()
    try:
        c.save()
        print("Salvataggio riuscito!")
    except:
        print("Errore! Salvataggio non riuscito!")"""

    # Modify Entry
    #car_to_modify = get_object_or_404(Car, model="Model2")
    #car_to_modify.model = "Lamborghini"
    #car_to_modify.save()

    # Delete element
    #car_to_modify.delete()

    return render(request,template_name=templ,context=ctx)

# Authentication functions

def is_a_driver(user):
    return user.groups.filter(name='Driver').exists()


# GARAGE ---------------------------------------------------

class CarsListView(GroupRequiredMixin, ListView):
    group_required = ["Driver" , "Passenger"]
    model = Car
    template_name = "garage.html"

    def get_queryset(self):
        return Car.objects.filter(user_id=self.request.user)

    
class CreateVehicleView(GroupRequiredMixin, CreateView):
    title = "Add a vehicle"
    group_required = ["Driver"]
    form_class = CreateVehicleForm
    template_name = "add_vehicle.html"
    success_url = reverse_lazy("home")

    # Set car owner (logged user)
    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super().form_valid(form)
    
class DeleteEntityView(DeleteView):
    template_name = "delete_vehicle.html"

    def get_context_data(self , **kwargs):
        ctx = super().get_context_data()
        # Car case
        if(self.model == Car):
            entity = "Car"
        ctx["entity"] = entity
        return ctx
    
    def get_success_url(self):
        if self.model == Car : 
            return reverse("home")

class DeleteCarView(GroupRequiredMixin , DeleteEntityView):
    title = "Delete a vehicle"
    group_required = ["Driver"]
    model = Car

class UpdateCarView(GroupRequiredMixin , UpdateView):
    title = "Modify vehicle settings"
    group_required = ["Driver"]
    model = Car
    template_name = "update_vehicle.html"
    fields = ["model" , "license_plate" , "km" , "last_inspection_date"]
    success_url = reverse_lazy("home")

# ----------------------------------------------------------------------


# TRIPS ----------------------------------------------------------------

class TripsListView(GroupRequiredMixin , ListView):
    group_required = ["Passenger" , "Driver"]
    model = Car
    template_name = "trips.html"

"""
class CreateTripView(GroupRequiredMixin, CreateView):
    title = "Create a new trip"
    group_required = ["Driver"]
    form_class = CreateTripForm
    template_name = "createtrip.html"
    success_url = reverse_lazy("home")
"""

@user_passes_test(is_a_driver)
def create_trip(request):
    
    # Post - Request
    if request.method == "POST":
        form = CreateTripForm(request.POST)
        if form.is_valid():
            car_id = form.cleaned_data.get("car")
            departure_location = form.cleaned_data.get("departure_location")
            arrival_location = form.cleaned_data.get("arrival_location")
            departure_time = form.cleaned_data.get("departure_time")
            arrival_time = form.cleaned_data.get("arrival_time")
            open_registration_time = form.cleaned_data.get("open_registration_time")
            close_registration_time = form.cleaned_data.get("close_registration_time")
            try:
                max_passenger = int(form.cleaned_data.get("max_passenger"))
            except:
                max_passenger = 0
            
            print("test : " , max_passenger)
            
            # Creation of Ride entry
            r = Ride()
            r.car = Car.objects.get(id = car_id)
            r.departure_location = departure_location
            r.arrival_location = arrival_location
            r.departure_time = departure_time
            r.arrival_time = arrival_time

            """
            b = Booking()
            b.open_registration_time = open_registration_time
            ...
            try:
                b.save()
            except:
                print("Error on booking save...")
            """
            #return redirect("polls:searchresults", sstring, where)
            
    else:  # GET - Request
        form = CreateTripForm(user = request.user)
    
    
    return render(request,template_name="createtrip.html",context={"form":form})

#-----------------------------------------------------------------------

