import requests
import time
from datetime import datetime
from zoneinfo import ZoneInfo
from math import sin, cos, sqrt, radians, asin

earth_radius = 6371 + 420 # km


def get_satellite_location():
    """This will return the ISS location"""

    url = "http://api.open-notify.org/iss-now.json"
    
    try:
        response = requests.get(url, timeout=5)
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


# calculate arc length for speed
def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two coordinates"""

    # degree --> radians
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    lat_diff = lat2 - lat1
    lon_diff = lon2 - lon1

    sq1 = sin(lat_diff / 2) ** 2
    sq2 = sin(lon_diff / 2) ** 2

    cq = cos(lat1) * cos(lat2)

    qty_root = sqrt(sq1 + cq * sq2)

    qty_sine_inv = asin(qty_root)

    distance = 2 * earth_radius * qty_sine_inv

    return distance


def get_speed(lat1, lon1, lat2, lon2, timestamp1, timestamp2):
    """It will calculate speed"""

    time_seconds = timestamp2 - timestamp1
    if time_seconds <= 0:
        return None

    distance = calculate_distance(lat1, lon1, lat2, lon2)
    speed = (distance / time_seconds) * 3600

    return speed


last_timestamp = None
last_longitude = None
last_latitude = None


while True:
    satellite_location = get_satellite_location()
    time_stamp = satellite_location["time"]
    longitude = satellite_location["longitude"]
    latitude = satellite_location["latitude"]

    # get the speed in kmph
    if last_timestamp is not None and time_stamp is not None:
        speed = get_speed(
            last_latitude,
            last_longitude,
            latitude,
            longitude,
            last_timestamp,
            time_stamp,
        )
    else:
        speed = None

    if time_stamp is not None:
        last_timestamp = time_stamp
        last_longitude = longitude
        last_latitude = latitude

    if time_stamp is not None:
        ist_time = datetime.fromtimestamp(time_stamp, ZoneInfo("Asia/Kolkata"))

        print(f"Time Stamp: {satellite_location['time']}")
        print(f"Time: {ist_time}")
        print(f"Longitude: {longitude}")
        print(f"Latitude: {latitude}")
        # print(f"Speed: {speed}")
        if speed is not None:
            print(f"Speed: {speed:.2f} km/h")
        else:
            print("speed: Calculating...")
    else:
        print("API Error")
        continue

    print("=" * 40)
    time.sleep(10)


