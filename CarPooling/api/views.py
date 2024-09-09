from django.shortcuts import render
from rest_framework import generics , viewsets , permissions
from gestione.models import Ride
from .serializers import RideSerializer

# class RideListAPIView(generics.ListAPIView): Alternative to viewsets

class RideViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, ) # This API is accessible only for logged user
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
