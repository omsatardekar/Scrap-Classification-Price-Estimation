from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="scrapx_app")

def reverse_geocode(lat: float, lon: float) -> str | None:
    try:
        location = geolocator.reverse((lat, lon), exactly_one=True)
        return location.address if location else None
    except Exception:
        return None
