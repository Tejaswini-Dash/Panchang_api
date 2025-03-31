# from app.calculations.astronomy import get_planetary_positions
# from app.calculations.sunrise_sunset import get_sun_times
# from app.calculations.tithi_nakshatra import get_tithi_nakshatra
# from app.calculations.rahu_yamaganda import get_rahu_yamaganda

# def compute_panchang(location, date_value):
#     """
#     Compute Panchang details for a given location and date.
#     """
#     sun_times = get_sun_times(location, date_value)
#     planetary_positions = get_planetary_positions(date_value)
#     tithi_nakshatra = get_tithi_nakshatra(date_value)
#     rahu_yamaganda = get_rahu_yamaganda(sun_times)

#     return {
#         "date": date_value,
#         "location": location,
#         "sun_times": sun_times,
#         "planetary_positions": planetary_positions,
#         "tithi_nakshatra": tithi_nakshatra,
#         "rahu_yamaganda": rahu_yamaganda
#     }



from app.calculations.astronomy import get_planetary_positions
from app.calculations.sunrise_sunset import get_sun_times
from app.calculations.tithi_nakshatra import get_tithi_nakshatra
from app.calculations.rahu_yamaganda import get_rahu_yamaganda

def compute_panchang(location, date_value):
    """
    Compute detailed Panchang data.
    """
    sun_times = get_sun_times(location, date_value)
    planetary_positions = get_planetary_positions(date_value)
    tithi_nakshatra = get_tithi_nakshatra(date_value)
    rahu_yamaganda = get_rahu_yamaganda(sun_times)

    return {
        "Panchang Details": {
            "Tithi": tithi_nakshatra["tithi"],
            "Nakshatra": tithi_nakshatra["nakshatra"],
            "Yoga": tithi_nakshatra["yoga"],
            "Karana": tithi_nakshatra["karana"],
            "Paksha": tithi_nakshatra["paksha"],
            "Day": date_value.strftime("%A"),
            "Dishashool": "EAST",  # Placeholder, compute dynamically if needed
            "Samvat": "1947 - Krodhi",
            "Vikram": "1947 - Krodhi"
        },
        "Panchang Timings": {
            "Gulika Kaal": "From {} To {}".format(sun_times["gulika_start"], sun_times["gulika_end"]),
            "Kulika Kaal": "From {} To {}".format(sun_times["gulika_start"], sun_times["gulika_end"]),
            "Yamaganda": "From {} To {}".format(sun_times["yamaganda_start"], sun_times["yamaganda_end"]),
            "Yamaghanta": "From {} To {}".format(sun_times["yamaganda_start"], sun_times["yamaganda_end"]),
            "Kaalvela / Ardhayaam": "From {} To {}".format(sun_times["kaalvela_start"], sun_times["kaalvela_end"]),
            "Rahu Kaal": "From {} To {}".format(sun_times["rahu_start"], sun_times["rahu_end"]),
            "Kantaka / Mrityu": "From {} To {}".format(sun_times["rahu_start"], sun_times["rahu_end"])
        }
    }

