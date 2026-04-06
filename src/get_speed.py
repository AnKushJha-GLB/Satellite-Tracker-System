from math import sin, cos, sqrt, radians, asin


earth_radius = 6371 + 420 # km

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