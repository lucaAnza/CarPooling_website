"""
URL configuration for CarPooling project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('home/' , home_page , name="homepage"),
    path("", home_page,name="homepage"),
    path("elenca/", elenca_params ,name="elenca"), # Parametri passati con ?
    path('parametri/<str:nome>/<int:eta>/', two_params, name='alias'),  # Parametri passati con /
    path('template/', hello_template, name='template'),
    path('database/', play_with_database , name='database'),
    path("garage/", CarsListView.as_view(), name="garage"),
    path("addvehicle/", CreateVehicleView.as_view() , name="addvehicle" ),
    path("deletevehicle/<pk>/" ,  DeleteCarView.as_view() , name="deletevehicle" ),
    path('updatevehicle/<pk>', UpdateCarView.as_view(), name="updatevehicle"),
    path("trips/<str>", TripsListView.as_view(), name="trips"),
    path("createtrip/", create_trip , name="createtrip" ),
    path("ridedetail/<pk>/", DatailRideView.as_view(), name="ridedetail"),
    path("ridedelete/<pk>/" , DeleteRideView.as_view() , name = "ridedelete"),
    path("searchtrip/" , search , name = "search_trip" ),
    path("searchtripresults/<str:string>/<str:where>/", SearchResultsList.as_view(), name="search_results_trip"),
    path('take_part/<int:pk>/', take_part, name='take_part'),
    path('leave_trip/<int:pk>/', leave_trip, name='leave_trip'),
    path('createreview/<int:pk>' , CreateReviewView.as_view() , name='create_review'),
    path('ranking/' , RankingView.as_view() , name='ranking' ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)