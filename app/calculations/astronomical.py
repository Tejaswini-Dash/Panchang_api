

from skyfield.api import load, wgs84
import pytz
from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from skyfield import almanac

# Load planetary ephemeris data
ts = load.timescale()
planets = load('de421.bsp')
earth, sun, moon = planets['earth'], planets['sun'], planets['moon']
tf = TimezoneFinder()

def calculate_day_duration(sunrise: str, sunset: str) -> float:
    """Calculate duration of daylight in hours"""
    sunrise_time = datetime.strptime(sunrise, '%H:%M:%S').time()
    sunset_time = datetime.strptime(sunset, '%H:%M:%S').time()
    
    sunrise_dt = datetime.combine(datetime.today(), sunrise_time)
    sunset_dt = datetime.combine(datetime.today(), sunset_time)
    
    return (sunset_dt - sunrise_dt).total_seconds() / 3600

def calculate_night_duration(moonrise: str, moonset: str) -> float:
    """Calculate duration of nighttime in hours"""
    moonrise_time = datetime.strptime(moonrise, '%H:%M:%S').time()
    moonset_time = datetime.strptime(moonset, '%H:%M:%S').time()
    
    moonrise_dt = datetime.combine(datetime.today(), moonrise_time)
    moonset_dt = datetime.combine(datetime.today(), moonset_time)
    
    return (moonset_dt - moonrise_dt).total_seconds() / 3600

def get_sun_moon_rise_set(place: str, date: str):
    geolocator = Nominatim(user_agent="panchang")
    location = geolocator.geocode(place)
    
    if not location:
        raise ValueError(f"Location {place} not found.")
    
    lat, lon = location.latitude, location.longitude
    tz_name = tf.timezone_at(lng=lon, lat=lat)
    
    if not tz_name:
        raise ValueError(f"Could not determine timezone for {place}. Using UTC.")
    
    time_zone = pytz.timezone(tz_name)
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    local_time = time_zone.localize(date_obj)

    observer = wgs84.latlon(lat, lon)

    # Compute sunrise and sunset times
    times, events = almanac.find_discrete(
        ts.utc(local_time.year, local_time.month, local_time.day),
        ts.utc(local_time.year, local_time.month, local_time.day, 23, 59, 59),
        almanac.sunrise_sunset(planets, observer)
    )

    rise_set_data = {}

    for t, event in zip(times, events):
        if event == 1:
            rise_set_data["sun_rise"] = t.astimezone(time_zone).strftime("%H:%M:%S")
        else:
            rise_set_data["sun_set"] = t.astimezone(time_zone).strftime("%H:%M:%S")

    # Compute moonrise and moonset times
    times, events = almanac.find_discrete(
        ts.utc(local_time.year, local_time.month, local_time.day),
        ts.utc(local_time.year, local_time.month, local_time.day, 23, 59, 59),
        almanac.risings_and_settings(planets, moon, observer)  
    )

    for t, event in zip(times, events):
        if event == 1:
            rise_set_data["moon_rise"] = t.astimezone(time_zone).strftime("%H:%M:%S")
        else:
            rise_set_data["moon_set"] = t.astimezone(time_zone).strftime("%H:%M:%S")

    # Calculate durations
    if 'sun_rise' in rise_set_data and 'sun_set' in rise_set_data:
        rise_set_data['day_duration'] = calculate_day_duration(rise_set_data['sun_rise'], rise_set_data['sun_set'])
    if 'moon_rise' in rise_set_data and 'moon_set' in rise_set_data:
        rise_set_data['night_duration'] = calculate_night_duration(rise_set_data['moon_rise'], rise_set_data['moon_set'])

    return rise_set_data
