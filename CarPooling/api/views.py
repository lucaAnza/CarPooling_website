from django.shortcuts import render
from rest_framework import generics
from gestione.models import Ride
from .serializers import RideSerializer


class RideListAPIView(generics.ListAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
