from django.urls import path
from .views import RideListAPIView


urlpatterns = [
    path('rides/', RideListAPIView.as_view()),
]