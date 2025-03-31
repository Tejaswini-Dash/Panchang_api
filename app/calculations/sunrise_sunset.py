# from skyfield.api import load, Topos
# from datetime import datetime

# def get_sun_times(location, date_value):
#     """
#     Compute sunrise and sunset times using Skyfield.
#     """
#     ts = load.timescale()
#     planets = load('de421.bsp')
#     earth, sun = planets['earth'], planets['sun']

#     # Example: If location is "lat,long" format, split it
#     lat, lon = map(float, location.split(",")) if "," in location else (0, 0)

#     observer = earth + Topos(latitude_degrees=lat, longitude_degrees=lon)
#     observer_time = ts.utc(date_value.year, date_value.month, date_value.day)

#     astrometric = observer.at(observer_time).observe(sun).apparent()
    
#     return {
#         "sunrise": str(observer_time.utc_datetime()),  # Placeholder (use solar calculations)
#         "sunset": str(observer_time.utc_datetime())    # Placeholder (use solar calculations)
#     }



from datetime import datetime, timedelta

def get_sun_times(location, date_value):
    """
    Compute sunrise, sunset, Rahu Kaal, Yamaganda, and other special timings.
    """
    # Placeholder sunrise & sunset times
    sunrise = datetime(date_value.year, date_value.month, date_value.day, 5, 22, 39)
    sunset = datetime(date_value.year, date_value.month, date_value.day, 18, 30, 0)

    # Compute various timings (based on placeholder logic, adjust accordingly)
    gulika_start = sunrise + timedelta(hours=3, minutes=7)
    gulika_end = gulika_start + timedelta(hours=1, minutes=33)

    yamaganda_start = sunrise
    yamaganda_end = sunrise + timedelta(hours=1, minutes=33)

    kaalvela_start = sunrise - timedelta(hours=1, minutes=33)
    kaalvela_end = sunrise

    rahu_start = kaalvela_start - timedelta(hours=1, minutes=33)
    rahu_end = kaalvela_start

    return {
        "sunrise": sunrise.strftime("%d-%m-%y %I:%M:%S %p"),
        "sunset": sunset.strftime("%d-%m-%y %I:%M:%S %p"),
        "gulika_start": gulika_start.strftime("%d-%m-%y %I:%M:%S %p"),
        "gulika_end": gulika_end.strftime("%d-%m-%y %I:%M:%S %p"),
        "yamaganda_start": yamaganda_start.strftime("%d-%m-%y %I:%M:%S %p"),
        "yamaganda_end": yamaganda_end.strftime("%d-%m-%y %I:%M:%S %p"),
        "kaalvela_start": kaalvela_start.strftime("%d-%m-%y %I:%M:%S %p"),
        "kaalvela_end": kaalvela_end.strftime("%d-%m-%y %I:%M:%S %p"),
        "rahu_start": rahu_start.strftime("%d-%m-%y %I:%M:%S %p"),
        "rahu_end": rahu_end.strftime("%d-%m-%y %I:%M:%S %p")
    }

