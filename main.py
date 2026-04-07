import time
from datetime import datetime
from zoneinfo import ZoneInfo


from src.tracking.get_satellite_location import get_satellite_location
from src.tracking.get_speed import get_speed
from src.config import TIMEZONE, UPDATE_INTERVAL


def main():
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
            ist_time = datetime.fromtimestamp(time_stamp, ZoneInfo(TIMEZONE))

            print(f"Time Stamp: {satellite_location['time']}")
            print(f"Time: {ist_time}")
            print(f"Longitude: {longitude:.4f}")
            print(f"Latitude: {latitude:.4f}")
            # print(f"Speed: {speed}")
            if speed is not None:
                print(f"Speed: {speed:.2f} km/h")
            else:
                print("speed: Calculating...")
        else:
            print("API Error")
            continue

        print("=" * 40) 
        time.sleep(UPDATE_INTERVAL)
        

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram stopped by user.")


