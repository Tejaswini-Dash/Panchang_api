

'''# from datetime import datetime
# from .astronomy import get_sun_position

# def calculate_panchang(place: str, date: str):
#     """
#     Dynamically calculate the Panchang for a given place and date.
#     """
#     try:
#         sun_altitude, sun_azimuth = get_sun_position(place, date)
#         date_obj = datetime.strptime(date, "%Y-%m-%d")

#         # Sample dynamic calculations for Panchang details
#         panchang_details = {
#             "date": date_obj.strftime('%d %B %Y'),
#             "place": place,
#             "sun_altitude": round(sun_altitude, 2),
#             "sun_azimuth": round(sun_azimuth, 2),
#             "tithi": "Tritiya",
#             "nakshatra": "Bharani",
#             "yoga": "Vishakumbha",
#             "karana": "Gar",
#             "paksha": "Shukla",
#             "day": date_obj.strftime('%A'),
#             "dishashool": "NORTH",
#             "samvat": "1947 - Krodhi",
#             "vikram": "1947 - Krodhi",
#             "timings": {
#                 "gulika_kaal": "08:29 AM - 10:02 AM",
#                 "kulika_kaal": "08:29 AM - 10:02 AM",
#                 "yamaganda": "05:22 AM - 06:55 AM",
#                 "yamaghanta": "05:22 AM - 06:55 AM",
#                 "kaalvela_ardhayaam": "03:48 AM - 05:22 AM",
#                 "rahu_kaal": "02:15 AM - 03:48 AM",
#                 "kantaka_mrityu": "02:15 AM - 03:48 AM"
#             }
#         }

#         return panchang_details
#     except Exception as e:
#         raise ValueError(f"Error in Panchang calculation: {str(e)}")
'''


from datetime import datetime
from .astronomy import get_sun_position
from skyfield.api import load
import math

# Load planetary data for calculations
planets = load('de421.bsp')
earth, moon, sun = planets['earth'], planets['moon'], planets['sun']

def calculate_panchang(place: str, date: str):
    """
    Dynamically calculate the Panchang for a given place and date.
    """
    try:
        # 🌞 Get Sun Position
        sun_altitude, sun_azimuth = get_sun_position(place, date)
        
        # 🕛 Convert Date
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        
        # 🛰 Compute Panchang Elements
        ts = load.timescale()
        t = ts.utc(date_obj.year, date_obj.month, date_obj.day)

        observer = earth
        sun_position = observer.at(t).observe(sun).apparent()
        moon_position = observer.at(t).observe(moon).apparent()

        sun_longitude = sun_position.ecliptic_latlon()[1].degrees
        moon_longitude = moon_position.ecliptic_latlon()[1].degrees

        # 📅 Calculate Tithi (Lunar Day)
        lunar_phase = (moon_longitude - sun_longitude) % 360
        tithi_number = math.floor(lunar_phase / 12) + 1  # 30 Tithis, 360° full moon cycle
        tithi_names = [
            "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami", "Shashthi", "Saptami", "Ashtami", 
            "Navami", "Dashami", "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Purnima",
            "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami", "Shashthi", "Saptami", "Ashtami", 
            "Navami", "Dashami", "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Amavasya"
        ]
        tithi = tithi_names[tithi_number - 1]

        # 🌠 Calculate Nakshatra (27 Lunar Mansions)
        # nakshatra_number = math.floor((moon_longitude / 13.3333))  # Each Nakshatra spans ~13.33°
        # nakshatra_names = [
        #     "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha",
        #     "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha",
        #     "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
        #     "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
        # ]
        # nakshatra = nakshatra_names[nakshatra_number]
        
        
        
        
        
        
        
        
        # # 🌠 Calculate Nakshatra (27 Lunar Mansions)
        # nakshatra_number = math.floor((moon_longitude % 360) / (360 / 27))
        # nakshatra_names = [
        # "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha",
        # "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha",
        # "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
        # "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
        # ]
        # nakshatra = nakshatra_names[nakshatra_number]

        ayanamsa = 24 + (4/60) + (60/3600)
        
        moon_sidereal_longitude = (moon_longitude - ayanamsa) % 360
        
        nakshatra_number = math.floor(moon_sidereal_longitude / (360 / 27))
        
        nakshatra_names = [
        "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha",
        "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha",
        "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
        "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
        ]

        nakshatra = nakshatra_names[nakshatra_number]














        # # 📏 Yoga Calculation (Sum of Sun & Moon longitudes / 13.33)
        # yoga_number = math.floor(((sun_longitude + moon_longitude) % 360) / 13.33)
        # yoga_names = [
        #     "Vishkumbha", "Priti", "Ayushman", "Saubhagya", "Shobhana", "Atiganda", "Sukarma", "Dhriti",
        #     "Shoola", "Ganda", "Vriddhi", "Dhruva", "Vyaghata", "Harshana", "Vajra", "Siddhi", "Vyatipata",
        #     "Variyana", "Parigha", "Shiva", "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma", "Indra", "Vaidhriti"
        # ]
        # yoga = yoga_names[yoga_number]


        # 📏 Calculate Yoga (Sum of Sun & Moon longitudes)
        yoga_number = math.floor(((sun_longitude + moon_longitude) % 360) / 13.3333)
        yoga_names = [
            "Vishkumbha", "Priti", "Ayushman", "Saubhagya", "Shobhana", "Atiganda", "Sukarma", "Dhriti",
            "Shoola", "Ganda", "Vriddhi", "Dhruva", "Vyaghata", "Harshana", "Vajra", "Siddhi", "Vyatipata",
            "Variyana", "Parigha", "Shiva", "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma", "Indra", "Vaidhriti"
        ]
        yoga = yoga_names[yoga_number]
        
        
        



        # # 🔢 Karana (Half of a Tithi, 60 per cycle)
        # karana_names = [
        #     "Bava", "Balava", "Kaulava", "Taitila", "Garaja", "Vanija", "Vishti", "Shakuni", "Chatushpada", "Naga",
        #     "Kimstughna"
        # ]
        # karana = karana_names[tithi_number % 11]


        # 🔢 Calculate Karana (Half of a Tithi, 60 per cycle)
        karana_names = [
            "Bava", "Balava", "Kaulava", "Taitila", "Garaja", "Vanija", "Vishti", "Shakuni", "Chatushpada", "Naga",
            "Kimstughna"
        ]
        karana_number = (tithi_number * 2) % 11
        karana = karana_names[karana_number]



        # 🌒 Paksha (Waxing or Waning Moon)
        paksha = "Shukla" if tithi_number <= 15 else "Krishna"

        # 🗓 Panchang Result
        panchang_details = {
            "date": date_obj.strftime('%d %B %Y'),
            "place": place,
            "sun_altitude": round(sun_altitude, 2),
            "sun_azimuth": round(sun_azimuth, 2),
            "tithi": tithi,
            "nakshatra": nakshatra,
            "yoga": yoga,
            "karana": karana,
            "paksha": paksha,
            "day": date_obj.strftime('%A'),
            "dishashool": "NORTH",  # Can be calculated dynamically in the future
            "samvat": "1947 - Krodhi",
            "vikram": "1947 - Krodhi",
            "timings": {
                "gulika_kaal": "08:29 AM - 10:02 AM",
                "kulika_kaal": "08:29 AM - 10:02 AM",
                "yamaganda": "05:22 AM - 06:55 AM",
                "yamaghanta": "05:22 AM - 06:55 AM",
                "kaalvela_ardhayaam": "03:48 AM - 05:22 AM",
                "rahu_kaal": "02:15 AM - 03:48 AM",
                "kantaka_mrityu": "02:15 AM - 03:48 AM"
            }
        }

        return panchang_details

    except Exception as e:
        raise ValueError(f"Error in Panchang calculation: {str(e)}")













# from datetime import datetime
# from .astronomy import get_sun_position
# from skyfield.api import load
# import math

# # Load planetary data for calculations
# planets = load('de421.bsp')
# earth, moon, sun = planets['earth'], planets['moon'], planets['sun']

# def calculate_panchang(place: str, date: str):
#     """
#     Dynamically calculate the Panchang for a given place and date.
#     """
#     try:
#         # Get Sun Position
#         sun_altitude, sun_azimuth = get_sun_position(place, date)
        
#         # Convert Date
#         date_obj = datetime.strptime(date, "%Y-%m-%d")
        
#         # Compute Panchang Elements
#         ts = load.timescale()
#         t = ts.utc(date_obj.year, date_obj.month, date_obj.day)

#         observer = earth
#         sun_position = observer.at(t).observe(sun).apparent()
#         moon_position = observer.at(t).observe(moon).apparent()

#         sun_longitude = sun_position.ecliptic_latlon()[1].degrees
#         moon_longitude = moon_position.ecliptic_latlon()[1].degrees

#         # Calculate Tithi (Lunar Day)
#         lunar_phase = (moon_longitude - sun_longitude) % 360
#         tithi_number = math.floor(lunar_phase / 12) + 1  # 30 Tithis in a lunar cycle
#         tithi_names = [
#             "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami", "Shashthi", "Saptami", "Ashtami", 
#             "Navami", "Dashami", "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Purnima",
#             "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami", "Shashthi", "Saptami", "Ashtami", 
#             "Navami", "Dashami", "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Amavasya"
#         ]
#         tithi = tithi_names[tithi_number - 1]

#         # Calculate Nakshatra (27 Lunar Mansions)
#         nakshatra_number = math.floor((moon_longitude % 360) / (360 / 27))
#         nakshatra_names = [
#             "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha",
#             "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha",
#             "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
#             "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
#         ]
#         nakshatra = nakshatra_names[nakshatra_number]

#         # Yoga Calculation (Sum of Sun & Moon longitudes / 13.33)
#         yoga_number = math.floor(((sun_longitude + moon_longitude) % 360) / 13.33)
#         yoga_names = [
#             "Vishkumbha", "Priti", "Ayushman", "Saubhagya", "Shobhana", "Atiganda", "Sukarma", "Dhriti",
#             "Shoola", "Ganda", "Vriddhi", "Dhruva", "Vyaghata", "Harshana", "Vajra", "Siddhi", "Vyatipata",
#             "Variyana", "Parigha", "Shiva", "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma", "Indra", "Vaidhriti"
#         ]
#         yoga = yoga_names[yoga_number]

#         # Karana (Half of a Tithi, 60 per cycle)
#         karana_names = [
#             "Bava", "Balava", "Kaulava", "Taitila", "Garaja", "Vanija", "Vishti", "Shakuni", "Chatushpada", "Naga",
#             "Kimstughna"
#         ]
#         karana = karana_names[tithi_number % 11]

#         # Paksha (Waxing or Waning Moon)
#         paksha = "Shukla" if tithi_number <= 15 else "Krishna"

#         # Panchang Result
#         panchang_details = {
#             "date": date_obj.strftime('%d %B %Y'),
#             "place": place,
#             "sun_altitude": round(sun_altitude, 2),
#             "sun_azimuth": round(sun_azimuth, 2),
#             "tithi": tithi,
#             "nakshatra": nakshatra,
#             "yoga": yoga,
#             "karana": karana,
#             "paksha": paksha,
#             "day": date_obj.strftime('%A'),
#             "dishashool": "NORTH",  # Placeholder, can be dynamically calculated
#             "samvat": "1947 - Krodhi",
#             "vikram": "1947 - Krodhi",
#             "timings": {
#                 "gulika_kaal": "08:29 AM - 10:02 AM",
#                 "kulika_kaal": "08:29 AM - 10:02 AM",
#                 "yamaganda": "05:22 AM - 06:55 AM",
#                 "yamaghanta": "05:22 AM - 06:55 AM",
#                 "kaalvela_ardhayaam": "03:48 AM - 05:22 AM",
#                 "rahu_kaal": "02:15 AM - 03:48 AM",
#                 "kantaka_mrityu": "02:15 AM - 03:48 AM"
#             }
#         }

#         return panchang_details

#     except Exception as e:
#         raise ValueError(f"Error in Panchang calculation: {str(e)}")
