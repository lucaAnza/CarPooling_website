from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import RideViewSet


router = SimpleRouter()
router.register('rides', RideViewSet, basename='rides')
urlpatterns = router.urls

""" Alternative
urlpatterns = [
    path('rides/', RideListAPIView.as_view()),
]
"""