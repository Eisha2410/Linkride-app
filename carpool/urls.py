from django.urls import path
from .rider_views import (
    RideListCreateAPIView,
    RideRetrieveUpdateDestroyAPIView,
    RideViewSet,
    JoinRideView,
    ride_check_in,
    ride_check_out,
)
from rest_framework.routers import DefaultRouter
from .user_views import RegisterUserAPIView

# Optional: ViewSet for admin or advanced frontend use
router = DefaultRouter()
router.register(r'rides', RideViewSet, basename='ride')

urlpatterns = router.urls + [
    # Rides list and creation
    path('rides/', RideListCreateAPIView.as_view(), name='ride-list-create'),

    # User registration
    path('register/', RegisterUserAPIView.as_view(), name='register'),

    # Ride detail, update, and delete
    path('rides/<int:pk>/', RideRetrieveUpdateDestroyAPIView.as_view(), name='ride-detail'),

    # Join a ride
    path('rides/<int:ride_id>/join/', JoinRideView.as_view(), name='join-ride'),

    # Ride check-in
    path('rides/<int:ride_id>/checkin/', ride_check_in, name='ride-check-in'),

    # Ride check-out
    path('rides/<int:ride_id>/checkout/', ride_check_out, name='ride-check-out'),

]