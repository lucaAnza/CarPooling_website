from django.db.models import Count, F
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
from django.contrib import messages

#Authentication
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin # pipenv install django-braces
from django.contrib.auth.decorators import user_passes_test

# Authentication functions

def is_a_driver(user):
    return user.groups.filter(name='Driver').exists()

    


# BASE - CLASS

class Update(UpdateView):
    
    template_name = "update.html"

    def form_valid(self, form):
        messages.success(self.request, "The update was completed successfully.")
        return super().form_valid(form)


# GARAGE ---------------------------------------------------

class CarsListView(GroupRequiredMixin, ListView):
    group_required = ["Driver" , "Passenger"]
    model = Car
    template_name = "garage.html"

    # Filter on database model
    def get_queryset(self):
        return Car.objects.filter(user=self.request.user)


class CreateVehicleView(GroupRequiredMixin, CreateView):
    title = "Add a vehicle"
    group_required = ["Driver"]
    form_class = CreateVehicleForm
    template_name = "add_vehicle.html"
    success_url = reverse_lazy("garage")

    # Set car owner (logged user)
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "You have successfully add a new car")
        return super().form_valid(form)

class DeleteCarView(GroupRequiredMixin , DeleteView):
    template_name = "delete_entity.html"
    title = "Delete a vehicle"
    group_required = ["Driver"]
    model = Car
    success_url = reverse_lazy("garage")

    # Check if the user is trying to delete an other car
    def dispatch(self, request, *args, **kwargs):
        car = self.get_object()
        if car.user != request.user:
            messages.error(request, "You tried to delete a car of another user. You will be reported to the admin! ⚠️")
            return redirect('garage')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        car = self.get_object()    
        rides = car.my_rides.all() 
        current_time = timezone.now()
        
        # Check if the car is used in this moment
        for r in rides:
            if current_time <= r.arrival_time: 
                messages.error(self.request, "This car cannot be deleted because it has active or upcoming rides.")
                return redirect('garage')  

        messages.success(self.request, "Car deleted successfully 🗑 ")
        return super().form_valid(form)


class UpdateCarView(GroupRequiredMixin , Update):
    title = "Modify vehicle settings"
    group_required = ["Driver"]
    model = Car
    form_class = UpdateCarForm
    success_url = reverse_lazy("garage")

    # Check if the user is trying to modify an other car
    def dispatch(self, request, *args, **kwargs):
        car = self.get_object()
        if car.user != request.user:
            messages.error(request, "You tried to modify a car of another user. You will be reported to the admin! ⚠️")
            return redirect('garage')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        car = self.get_object()    
        messages.success(self.request, "Car modified successfully 🛠️ ")
        return super().form_valid(form)

# ----------------------------------------------------------------------


# TRIPS ----------------------------------------------------------------
@login_required
def leave_trip(request, pk):
    # Find the trip and ensure the user is a passenger
    passenger = get_object_or_404(Passenger, ride_id=pk, user=request.user)

    ride = Ride.objects.get(id = pk)
    if(ride.is_running()):
        messages.error(request, "You can't leave a trip while is running")
        return redirect("home")
    try:
        passenger.delete()  # Remove the user from the trip
        messages.success(request, "You have successfully left the trip.")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")

    # Reload the current page (user's trip list)
    return redirect(reverse('trips', kwargs={'str': 'passenger'}))

class TripsListView(GroupRequiredMixin , ListView):
    group_required = ["Passenger" , "Driver"]
    model = Ride
    template_name = "trips_passenger.html"

    # Choose template
    def get_template_names(self):
        trip_type = self.kwargs.get('str')
        if trip_type == 'driver':
            return ["trips_driver.html"]
        elif trip_type == 'passenger':
            return ["trips_passenger.html"]
        elif trip_type == 'old':
            return ["trips_old.html"]
        else:
            return ["home.html"]

    # Get the last {limit} elements
    def get_queryset(self):
        trip_type = self.kwargs.get('str')
        limit = 6
        if trip_type == 'driver':
            # Show only incoming rides
            current_time = timezone.now()
            rides = Ride.objects.filter(  arrival_time__gte=current_time ) 
            return rides.filter(user=self.request.user).order_by('-id')[:limit]
        elif trip_type == 'passenger':
            return Passenger.objects.filter(user=self.request.user , ride__arrival_time__gt=timezone.now()).order_by('-id')[:limit]
        elif trip_type == 'old':
            #TODO -> FINISH CHECK
            set1 = Ride.objects.filter(arrival_time__lt=timezone.now() , passengers__user = self.request.user).order_by('-id')
            set2 = Ride.objects.filter(arrival_time__lt=timezone.now() , user = self.request.user).order_by('-id')
            final_set = set1 | set2
            final_set = final_set.distinct()
            final_set = final_set[:limit]
            return final_set
        else:
            return None
        

@login_required
@user_passes_test(is_a_driver)
def create_trip(request):
    if request.method == "POST":
        form = CreateTripForm(request.POST, request.FILES,  user=request.user )
        if form.is_valid():
            car = form.cleaned_data.get("car")
            departure_location = form.cleaned_data.get("departure_location")
            departure_state = form.cleaned_data.get("departure_state")
            departure_address = form.cleaned_data.get("departure_address")
            arrival_location = form.cleaned_data.get("arrival_location")
            arrival_state = form.cleaned_data.get("arrival_state")
            arrival_address = form.cleaned_data.get("arrival_address")
            departure_time = form.cleaned_data.get("departure_time")
            arrival_time = form.cleaned_data.get("arrival_time")
            open_registration_time = form.cleaned_data.get("open_registration_time")
            close_registration_time = form.cleaned_data.get("close_registration_time")
            max_passenger = form.cleaned_data.get("max_passenger")
            image = form.cleaned_data.get("image")

            # Creation of Ride entry
            ride = Ride(
                car=car,
                departure_location=departure_location,
                departure_state = departure_state,
                departure_address = departure_address,
                arrival_location=arrival_location,
                arrival_state = arrival_state,
                arrival_address = arrival_address,
                departure_time=departure_time,
                arrival_time=arrival_time,
                user=request.user,
                open_registration_time=open_registration_time,
                close_registration_time=close_registration_time,
                max_passenger=max_passenger,
                image = image
            )
            try:
                ride.save()
                messages.success(request, "You have successfully add a new trip.")
                return redirect("home")
            except Exception as e:
                print(f"Error on ride save: {e}")
                messages.error(request, "Error - Please contact the amministrator")
                form.add_error(None, "An error occurred while saving the ride. Please try again.")
                return redirect("home")
        else:
            messages.error(request, "Error - Check the compiled form")
    else:
        form = CreateTripForm(user=request.user)

    ctx = {
        'form': form,
        'title': 'Create a New Trip'  
    }
    return render(request, "createtrip.html", context = ctx )


class DatailRideView(GroupRequiredMixin , DetailView):
    title = "Ride detail"
    group_required = ["Passenger" , "Driver"]
    model = Ride
    template_name = "ride_detail.html"

    # Check if the user is trying to get information of other rides
    def dispatch(self, request, *args, **kwargs):
        ride = self.get_object()
        if(ride.is_finish()):
            p = Passenger.objects.filter(user = request.user , ride = ride )
            if ride.user != request.user and len(p) == 0:
                messages.error(request, "You tried to get trip detail of another user. You will be reported to the admin! ⚠️ ")
                return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    #Back button
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Recover the url
        referrer = self.request.META.get('HTTP_REFERER', '/')
        context['referrer'] = referrer
        return context

class DeleteRideView(GroupRequiredMixin , DeleteView):
    template_name = "delete_entity.html"
    title = "Delete a ride"
    group_required = ["Driver"]
    model = Ride
    success_url = reverse_lazy("home")

    # Check if the user is trying to delete an other ride
    def dispatch(self, request, *args, **kwargs):
        ride = self.get_object()
        print(ride , "---" , request.user , "---" , ride.user)
        if ride.user != request.user:
            messages.error(request, "You tried to delete a trip of another user. You will be reported to the admin! ⚠️ ")
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    # Delete elements linked with the ride
    def post(self, request, *args, **kwargs):
        messages.success(self.request, "Trip deleted successfully 🗑")
        response = super().delete(request, *args, **kwargs)
        return response

#-----------------------------------------------------------------------



# RESEARCH--------------------------------------------------------------

def get_filtered_rides(user=None, search_string=None, search_where=None , limit = 9):
    current_time = timezone.now()
    # Base queryset: Rides that are valid (open for registration, not full)
    rides = Ride.objects.filter(
        open_registration_time__lte=current_time,  # Ride has opened registration
        close_registration_time__gte=current_time  # Ride has not closed registration
    ).annotate(
        passenger_count=Count('passengers')  # Count the number of passengers in each ride
    ).filter(
        passenger_count__lt=F('max_passenger')  # Only include rides that are not full
    )

    # Exclude rides where the logged-in user is the owner
    if user and user.is_authenticated:
        rides = rides.exclude(user_id=user)
        # Exclude rides where the user is already a passenger
        rides = rides.exclude(passengers__user=user)

    # Apply the filter based on the user's selection
    if search_string and search_where:
        if search_where == "Destination":
            rides  = rides.filter(arrival_location__icontains = search_string)
        elif search_where == "Departure":
            rides = rides.filter(departure_location__icontains = search_string)

    return rides[:limit]

def search(request):
    if request.method == "POST":
        form = SearchTripForm(request.POST)
        if form.is_valid():
            where = form.cleaned_data.get("search_where")
            string = form.cleaned_data.get("search_string")

            # Apply filters and redirect to results page
            return redirect("search_results_trip", string=string, where=where , limit = 18)
    else:
        form = SearchTripForm()

    # Get the filtered trips for the initial load
    trips = get_filtered_rides(user=request.user)

    return render(request, "search_trip.html", context={"form": form, "title": "Search", "trips": trips})

class SearchResultsList(ListView):
    model = Ride
    template_name = "search_results_trip.html"

    def get_queryset(self):
        string = self.request.resolver_match.kwargs["string"]
        where = self.request.resolver_match.kwargs["where"]

        # Apply filters based on query parameters
        return get_filtered_rides(user=self.request.user, search_string=string, search_where=where)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['where'] = self.request.resolver_match.kwargs["where"]
        context['string'] = self.request.resolver_match.kwargs["string"]
        return context


#-----------------------------------------------------------------------

# PASSENGERS------------------------------------------------------------

@login_required
def take_part(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to take part in a trip.")
        return redirect('search_trip')

    ride = get_object_or_404(Ride, pk=pk)
    user = request.user

    # Check if the user is the owner of the trip
    if ride.user_id == user.pk:
        messages.error(request, "You can't go on your own trip.")
    # Check if there are seats available in the car
    elif ride.passengers.count() >= ride.max_passenger:
        messages.error(request, "The trip is already full.")
    # Check if the user is already in that ride
    elif Passenger.objects.filter(user=user, ride=ride).exists():
        messages.error(request, "You are already signed up for this trip.")
    else:
        # If no errors, add the passenger
        try:
            Passenger.objects.create(user=user, ride=ride)
            messages.success(request, "You have been added to the trip successfully!")
        except Exception as e:
            print("Error! " + str(e))
            messages.error(request, "Error adding to trip.")

    return redirect('home')
#-----------------------------------------------------------------------



# REVIEW ---------------------------------------------------------------

class CreateReviewView(GroupRequiredMixin, CreateView):
    title = "Review"
    group_required = ["Driver" , "Passenger"]
    form_class = CreateReviewForm
    template_name = "createreview.html"
    success_url = reverse_lazy("home")

    # Add ride_id to the context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ride_id'] = self.kwargs['pk']
        return context

    # Check on ride_id + add review on Ride table
    def form_valid(self, form):
        ride_id = self.kwargs['pk']
        if Ride.objects.filter(id = ride_id , user = self.request.user):
            form.add_error(None, "You try to review yourself! You cant!")
            return self.form_invalid(form)
            
        # Check if the ride exists in the Ride table of the logged user
        if not Passenger.objects.filter(ride=ride_id , user = self.request.user).exists():
            form.add_error(None, "The specified ride does not exist for the logged user!")
            return self.form_invalid(form)

        # Get review from the form
        review = form.save()
        # Get the passenger
        passenger = Passenger.objects.get(ride=ride_id, user=self.request.user)
        # Set the review to the passenger
        passenger.review_id = review
        passenger.save()

        messages.success(self.request, "Review added successfully!")
        return super().form_valid(form)

@login_required
def show_review(request , pk):
    ride_id = pk
    passengers = Passenger.objects.filter(ride = ride_id).exclude(review_id = None)
    
    # Back button
    referrer = request.META.get('HTTP_REFERER', '/')

    # Calculate medium of all ratings
    sum = 0
    count = 0
    result = 0
    for p in passengers:
        if(p.review_id):
            sum = sum + p.review_id.rating
            count = count + 1
    if(count != 0):
        result = int(sum / count)
    # Context
    ctx = {
        'title': 'Reviews',
        'object_list' : passengers,
        'rating_sum' : result,
        'ride_id' : ride_id,
        'referrer' : referrer,
    }
    return render(request, "reviews.html", context = ctx )

class UpdateReviewView(GroupRequiredMixin , Update):
    title = "Modify your review"
    group_required = ["Driver" , "Passenger"]
    model = Review
    form_class = CreateReviewForm
    success_url = reverse_lazy("home")

    # Check if the user is trying to modify an other review
    def dispatch(self, request, *args, **kwargs):
        #Check if the logged user is in that specific trip
        review = self.get_object()
        list_of_reviewers = review.reviewers.filter(user = self.request.user)

        if len(list_of_reviewers) == 0:
            messages.error(request, "You tried to modify a review of another user. You will be reported to the admin! ⚠️ ")
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
#-----------------------------------------------------------------------




# RANKING ---------------------------------------------------------------

class RankingView(ListView):
    model = User
    template_name = "drivers_ranking.html"
    title = "Ranking"

    def get_queryset(self):
        raw_query = """
            SELECT  auth_user.id , auth_user.username, COUNT(gestione_ride.id) as ride_count
            FROM auth_user
            LEFT JOIN gestione_ride ON auth_user.id = gestione_ride.user_id
            GROUP BY auth_user.id, auth_user.username
            ORDER BY ride_count DESC
            LIMIT 5
        """
        return User.objects.raw(raw_query)

    
#-----------------------------------------------------------------------

# MY-PROFILE ------------------------------------------------------------

class MyProfileView(GroupRequiredMixin , ListView):
    group_required = ["Passenger", "Driver"]
    model = User
    template_name = "profile.html"
    title = "My Profile"

#-----------------------------------------------------------------------