import requests

from ..config import ISS_URL_API

def get_satellite_location():
    """This will return the ISS location"""

    # url = "http://api.open-notify.org/iss-now.json"
    
    try:
        response = requests.get(ISS_URL_API, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        
        location = {
            "time": data["timestamp"],
            "longitude": float(data["iss_position"]["longitude"]),
            "latitude": float(data["iss_position"]["latitude"]),
        }
    except requests.exceptions.RequestException:
        location = {
            "time": None,
            "longitude": None,
            "latitude": None,
        }
    
    
    return location