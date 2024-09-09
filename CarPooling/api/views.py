from django.shortcuts import render
from rest_framework import generics , viewsets
from gestione.models import Ride
from .serializers import RideSerializer

# class RideListAPIView(generics.ListAPIView): Alternative to viewsets

class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
