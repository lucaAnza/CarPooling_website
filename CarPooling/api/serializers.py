from rest_framework import serializers
from gestione.models import Ride

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ["id", "arrival_location" , "departure_location"]