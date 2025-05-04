import requests
from django.conf import settings

def get_distance_km(origin, destination):
    """
    Uses Google Distance Matrix API to calculate driving distance between two places.
    Returns distance in kilometers (float).
    """
    base_url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": origin,
        "destinations": destination,
        "units": "metric",
        "key": settings.GOOGLE_MAPS_API_KEY
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    try:
        distance_text = data['rows'][0]['elements'][0]['distance']['text']  # e.g., "12.3 km"
        distance_km = float(distance_text.replace(" km", "").replace(",", ""))
        return distance_km
    except (KeyError, IndexError, ValueError):
        return 0.0