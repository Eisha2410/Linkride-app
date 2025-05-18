from django.urls import path, include 
from .rider_views import (
    RideListCreateAPIView,
    RideRetrieveUpdateDestroyAPIView,
    RideViewSet,
    JoinRideView,
)
from rest_framework.routers import DefaultRouter
from .user_views import RegisterUserAPIView

# Optional: ViewSet for admin or advanced frontend use
router = DefaultRouter()
router.register(r'rides', RideViewSet)


urlpatterns = router.urls + [
    # Rides list and creation
    path('rides/', RideListCreateAPIView.as_view(), name='ride-list-create'),
    
    path('', include(router.urls)),
    
    # User registration
    path('register/', RegisterUserAPIView.as_view(), name='register'),

    # Ride detail, update, and delete
    path('rides/<int:pk>/', RideRetrieveUpdateDestroyAPIView.as_view(), name='ride-detail'),

    # Join a ride
    path('rides/<int:ride_id>/join/', JoinRideView.as_view(), name='join-ride'),

]