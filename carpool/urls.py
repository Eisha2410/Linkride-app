from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from .views import RideListCreateAPIView, RideRetrieveUpdateDestroyAPIView, RideViewSet
from .views import RegisterUserAPIView, JoinRideView

router = DefaultRouter()
router.register(r'rides', RideViewSet, basename='ride')

urlpatterns = router.urls

urlpatterns = [
    path('rides/', RideListCreateAPIView.as_view(), name='ride-list-create'),
    path('register/', RegisterUserAPIView.as_view(), name='register'),
    path('rides/<int:pk>/', RideRetrieveUpdateDestroyAPIView.as_view(), name='ride-detail'),
    path('rides/<int:ride_id>/join/', JoinRideView.as_view(), name='join-ride'),
    path('rides/<int:ride_id>/checkin/', views.ride_check_in, name='ride-check-in'),
    path('rides/<int:ride_id>/checkout/', views.ride_check_out, name='ride-check-out'),
]