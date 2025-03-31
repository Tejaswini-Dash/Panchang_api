from skyfield.api import load

def get_planetary_positions(date_value):
    """
    Compute planetary positions using Skyfield.
    """
    ts = load.timescale()
    planets = load('de421.bsp')

    earth, moon, sun = planets['earth'], planets['moon'], planets['sun']
    observer_time = ts.utc(date_value.year, date_value.month, date_value.day)

    positions = {
        "sun": earth.at(observer_time).observe(sun).apparent().ecliptic_latlon(),
        "moon": earth.at(observer_time).observe(moon).apparent().ecliptic_latlon()
    }

    return {
        "sun_position": positions["sun"][1].degrees,
        "moon_position": positions["moon"][1].degrees
    }
