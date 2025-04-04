import requests
import os
from dotenv import load_dotenv
from astral import LocationInfo
from astral.sun import sun
from datetime import datetime, timedelta
import pytz
from timezonefinder import TimezoneFinder

# Load API key securely
load_dotenv()
google_api_key = os.getenv("GOOGLE_MAPS_API_KEY")

if not google_api_key:
    raise ValueError("Missing Google Maps API Key! Set it as an environment variable.")

def get_lat_long_from_place(place_name: str) -> tuple:
    """
    Returns (latitude, longitude) from a place string using Google Maps Geocoding.
    """
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": place_name, "key": google_api_key}

    try:
        resp = requests.get(base_url, params=params)
        data = resp.json()

        if data.get("status") != "OK":
            raise ValueError(f"Geocoding API error: {data.get('status')} - {data.get('error_message', 'No details')}")

        location = data["results"][0]["geometry"]["location"]
        return location["lat"], location["lng"]
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error in Geocoding request: {str(e)}")

def get_timezone(lat, lng):
    tf = TimezoneFinder()
    return tf.timezone_at(lng=lng, lat=lat) or "UTC"

def get_sun_times(date_obj: datetime, place_name: str):
    """ Get correct sunrise and sunset times with timezone adjustments. """
    lat, lng = get_lat_long_from_place(place_name)
    timezone = get_timezone(lat, lng)
    
    location = LocationInfo(name=place_name, region="", timezone=timezone, latitude=lat, longitude=lng)
    s = sun(location.observer, date=date_obj.date(), tzinfo=location.timezone)

    return s["sunrise"], s["sunset"]

def get_panchang_timings(date_obj: datetime, place_name: str) -> dict:
    """ Fixes Gulika Kalam being one segment ahead. """
    sunrise, sunset = get_sun_times(date_obj, place_name)

    day_duration = (sunset - sunrise) / 8

    time_segment_map = {
        "Monday":  [2, 7, 5],  # [Rahu, Gulika, Yamaganda]
        "Tuesday": [7, 6, 6],
        "Wednesday": [5, 5, 4],
        "Thursday": [6, 4, 3],
        "Friday": [4, 3, 2],
        "Saturday": [3, 2, 7],
        "Sunday": [8, 1, 8],
    }

    weekday = date_obj.strftime("%A")
    rahu_segment, gulika_segment, yamaganda_segment = time_segment_map[weekday]

    # Compute each period
    rahu_start = sunrise + (rahu_segment - 1) * day_duration
    rahu_end = rahu_start + day_duration

    # 🛠 FIX: Shift Gulika Kalam one segment back
    gulika_start = sunrise + (gulika_segment - 2) * day_duration  # -1 correction
    gulika_end = gulika_start + day_duration

    yamaganda_start = sunrise + (yamaganda_segment - 3) * day_duration
    yamaganda_end = yamaganda_start + day_duration

    return {
        "Rahu Kalam": f"{rahu_start.strftime('%I:%M %p')} to {rahu_end.strftime('%I:%M %p')}",
        "Gulika Kalam": f"{gulika_start.strftime('%I:%M %p')} to {gulika_end.strftime('%I:%M %p')}",  # ✅ FIXED!
        "Yamaganda": f"{yamaganda_start.strftime('%I:%M %p')} to {yamaganda_end.strftime('%I:%M %p')}"
    }

