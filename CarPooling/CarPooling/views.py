from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
# User-Groups models
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
# Top destination import
from gestione.models import Ride
from django.db.models import Count,Max


# Function for authentication
def is_a_passenger(user):
    return user.groups.filter(name='Passenger').exists()

# Function Based View (FBV)
def home_page(request):

    #top_destinations = Ride.objects.all
    
    
    # Get top destinations
    top_destination = Ride.objects.raw("""
        SELECT id, arrival_location, COUNT(id) as count, MAX(image) as max_img
        FROM gestione_ride
        GROUP BY arrival_location
        ORDER BY count DESC
        LIMIT 3
    """)

    ctx = { "top_destination": top_destination}
    return render(request, template_name="home.html" , context=ctx)

class UserCreateView(CreateView):
    form_class = CreateUserPassenger
    template_name = "user_create.html"
    messages = "You have successfully create a new Account. Please Login "
    success_url = reverse_lazy("login?msg=success")

@user_passes_test(is_a_passenger)
def createDriver(request):
    ctx= { "title" : "Hi" }
    user = get_object_or_404(User, pk=request.user.pk)  # Get logged user
    gruppo_driver , created = Group.objects.get_or_create(name='Driver') # Get reference of driver group
    user.groups.add(gruppo_driver) # Add user to the group
    return render(request, template_name = 'driver_create.html' , context = ctx)