import requests

def reverse_geocode(lat: float, lon: float):
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        "lat": lat,
        "lon": lon,
        "format": "json"
    }
    headers = {
        "User-Agent": "ScrapX/1.0 (educational project)"
    }

    try:
        res = requests.get(url, params=params, headers=headers, timeout=5)
        if res.status_code != 200:
            return None

        data = res.json()
        address = data.get("address", {})

        return {
            "display_name": data.get("display_name"),
            "city": address.get("city") or address.get("town") or address.get("village"),
            "state": address.get("state"),
            "country": address.get("country"),
            "postcode": address.get("postcode"),
        }

    except Exception:
        return None
