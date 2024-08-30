from django.contrib import admin
from .models import *

# Registered Models
admin.site.register(Car)
admin.site.register(Ride)
admin.site.register(Passenger)
admin.site.register(Review)