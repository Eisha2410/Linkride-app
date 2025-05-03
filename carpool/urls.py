from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from .views import RideListCreateAPIView, RideRetrieveUpdateDestroyAPIView, RideViewSet
from .views import RegisterUserAPIView, JoinRideView

# FRONTEND: (Optional use)
# ViewSet for advanced use in frontend if needed (e.g. driver profile)
# Not used if individual views are sufficient
router = DefaultRouter()
router.register(r'rides', RideViewSet, basename='ride')

urlpatterns = router.urls

urlpatterns = [
    # - Rides listing page (GET)
    # - Create ride form (POST)
    # Used on home page or "Available Rides" section
    path('rides/', RideListCreateAPIView.as_view(), name='ride-list-create'),
    
    # FRONTEND:
    # - User registration page/form
    # Used on signup screen
    path('register/', RegisterUserAPIView.as_view(), name='register'),
  
    # FRONTEND:
    # - Ride details page (GET)
    # - Edit ride button (PUT/PATCH)
    # - Delete ride button (DELETE)
    path('rides/<int:pk>/', RideRetrieveUpdateDestroyAPIView.as_view(), name='ride-detail'),
    
    # FRONTEND:
    # - "Join Ride" button on ride card/details
    path('rides/<int:ride_id>/join/', JoinRideView.as_view(), name='join-ride'),
   
    # FRONTEND:
    # - "Check-In" button (when starting the ride)
    path('rides/<int:ride_id>/checkin/', views.ride_check_in, name='ride-check-in'),
    
    # FRONTEND:
    # - "Check-Out" button (when ending the ride)
    path('rides/<int:ride_id>/checkout/', views.ride_check_out, name='ride-check-out'),
]