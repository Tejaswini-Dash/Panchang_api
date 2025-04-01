# from skyfield.api import load, Topos
# import pytz
# from datetime import datetime

# # Load planetary ephemeris data
# planets = load('de421.bsp')
# earth = planets['earth']

# def get_sun_position(place: str, date: str):
#     """
#     Calculate the Sun's position for a given place and date.
#     """
#     # Load geographic location of the place using Geopy
#     from geopy.geocoders import Nominatim
#     geolocator = Nominatim(user_agent="panchang")
#     location = geolocator.geocode(place)
    
#     if not location:
#         raise ValueError(f"Location {place} not found.")
    
#     lat = location.latitude
#     lon = location.longitude
#     time_zone = pytz.timezone(location.raw['address'].get('timezone', 'UTC'))
    
#     # Calculate the time for given date and location
#     local_time = datetime.strptime(date, "%Y-%m-%d")  # Example format: 2025-04-01
#     local_time = time_zone.localize(local_time)
#     t = load.timescale().utc(local_time.year, local_time.month, local_time.day, local_time.hour, local_time.minute, local_time.second)
    
#     observer = earth.at(Topos(latitude_degrees=lat, longitude_degrees=lon))
#     sun = planets['sun']
#     astrometric = observer.at(t).observe(sun)
    
#     # Get the sun's altitude and azimuth
#     altitude, azimuth, _ = astrometric.apparent().altaz()
    
#     return altitude.degrees, azimuth.degrees




# from skyfield.api import load, wgs84
# import pytz
# from datetime import datetime
# from geopy.geocoders import Nominatim

# # Load planetary ephemeris data
# planets = load('de421.bsp')
# earth = planets['earth']
# tf = TimezoneFinder()


# def get_sun_position(place: str, date: str):
#     """
#     Calculate the Sun's position for a given place and date.
#     """
#     geolocator = Nominatim(user_agent="panchang")
#     location = geolocator.geocode(place)
    
#     if not location:
#         raise ValueError(f"Location {place} not found.")
    
#     lat, lon = location.latitude, location.longitude
#     tz_name = location.raw['display_name'].split(',')[-1].strip()
#     time_zone = pytz.timezone(tz_name) if tz_name else pytz.utc

#     # Convert date string to localized datetime
#     local_time = datetime.strptime(date, "%Y-%m-%d")
#     local_time = time_zone.localize(local_time)

#     # Get Skyfield time
#     ts = load.timescale()
#     t = ts.utc(local_time.year, local_time.month, local_time.day)

#     observer = earth + wgs84.latlon(lat, lon)
#     sun = planets['sun']
#     astrometric = observer.at(t).observe(sun)

#     # Get Sun's altitude and azimuth
#     altitude, azimuth, _ = astrometric.apparent().altaz()

#     return altitude.degrees, azimuth.degrees





from skyfield.api import load, wgs84
import pytz
from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

# Load planetary ephemeris data
planets = load('de421.bsp')
earth = planets['earth']
tf = TimezoneFinder()

def get_sun_position(place: str, date: str):
    """
    Calculate the Sun's position for a given place and date.
    """
    geolocator = Nominatim(user_agent="panchang")
    location = geolocator.geocode(place)
    
    if not location:
        raise ValueError(f"Location {place} not found.")
    
    lat, lon = location.latitude, location.longitude
    
    # Get timezone using timezonefinder
    tz_name = tf.timezone_at(lng=lon, lat=lat)
    
    if not tz_name:
        raise ValueError(f"Could not determine timezone for {place}. Using UTC.")
    
    time_zone = pytz.timezone(tz_name)

    # Convert date string to localized datetime
    local_time = datetime.strptime(date, "%Y-%m-%d")
    local_time = time_zone.localize(local_time)

    # Get Skyfield time
    ts = load.timescale()
    t = ts.utc(local_time.year, local_time.month, local_time.day)

    observer = earth + wgs84.latlon(lat, lon)
    sun = planets['sun']
    astrometric = observer.at(t).observe(sun)

    # Get Sun's altitude and azimuth
    altitude, azimuth, _ = astrometric.apparent().altaz()

    return round(altitude.degrees, 2), round(azimuth.degrees, 2)
