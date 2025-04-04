from datetime import datetime, timedelta
from app.calculations.astronomical import get_sun_moon_rise_set, calculate_day_duration
from .sunriseset import get_panchang_timings
from skyfield.api import load
import math

# Load planetary data
planets = load('de421.bsp')
earth, moon, sun = planets['earth'], planets['moon'], planets['sun']

# Correct 60-year cycle names with proper alignment (Prabhava = 1987-88)
SAMVAT_NAMES = [
    "Prabhava", "Vibhava", "Shukla", "Pramoda", "Prajapati", "Angirasa", "Shrimukha", "Bhava",
    "Yuvan", "Dhatri", "Ishvara", "Bahudhanya", "Pramadi", "Vikrama", "Vrisha", "Chitrabhanu",
    "Svabhanu", "Tarana", "Parthiva", "Vyaya", "Sarvajit", "Sarvadhari", "Virodhi", "Vikriti",
    "Khara", "Nandana", "Vijaya", "Jaya", "Manmatha", "Durmukhi", "Hevilambi", "Vilambi",
    "Vikari", "Sharvari", "Plava", "Shubhakrit", "Shobhana", "Krodhi", "Vishvavasu", "Parabhava",
    "Plavanga", "Keelaka", "Saumya", "Sadharan", "Virodhikrit", "Paridhavi", "Pramadicha",
    "Ananda", "Rakshasa", "Nala", "Pingala", "Kalayukti", "Siddharthi", "Raudra", "Durmati",
    "Dundubhi", "Rudhirodgari", "Raktakshi", "Krodhana", "Kshaya"
]

SPECIAL_CASES = {
    "shaka": {
        # 1940s
        # 1916: "Bhava",
        # 1945: "Krodhana",
        # 1946: "Kshaya",
        # 1947: "Vishvavasu",
        # 1948: "Parabhava",
        # 1949: "Plavanga",
        # # 1950s
        # 1950: "Kilaka",
        # 1951: "Saumya",
        # 1952: "Sadharan",
        # 1953: "Virodhikrit",
        # 1954: "Paridhavi",
        # 1955: "Pramadicha",
        # 1956: "Ananda",
        # 1957: "Rakshasa",
        # 1958: "Nala",
        # 1959: "Pingala",
        # # 1960s
        # 1960: "Kalayukti",
        # 1961: "Siddharthi",
        # 1962: "Raudra",
        # 1963: "Durmati"
    },
    "vikram": {
        # # 2080s
        # 2080: "Vishvavasu",
        # 2081: "Parabhava",
        # 2082: "Kalayukta",
        # 2083: "Siddharthi",
        # 2084: "Raudra",
        # 2085: "Dundubhi",
        # 2086: "Rudhirodgari",
        # 2087: "Raktakshi",
        # 2088: "Krodhana",
        # 2089: "Kshaya",
        # # 2090s
        # 2090: "Prabhava",
        # 2091: "Vibhava",
        # 2092: "Shukla",
        # 2093: "Pramoda",
        # 2094: "Prajapati",
        # 2095: "Angirasa",
        # # Historical (for reference)
        # 2051: "Sarvajit",
        # 2052: "Bahudhanya",
        # 2053: "Pramadi"
    }
}

def get_samvat_name(era_type, year):
    """Get name with manual corrections for problematic years"""
    if era_type in SPECIAL_CASES and year in SPECIAL_CASES[era_type]:
        return SPECIAL_CASES[era_type][year]
    # Dynamic calculation for other years
    base_year = 1987  # Prabhava start year
    cycle_pos = (year - base_year) % 60
    return SAMVAT_NAMES[cycle_pos]



def get_samvat_details(date_obj):
    greg_year = date_obj.year
    month = date_obj.month
    # Year calculations based on month
    vikram_year = greg_year + 57 if month >= 4 else greg_year + 56
    shaka_year = greg_year - 78 if month >= 4 else greg_year - 79

    return {
        "vikram_year": vikram_year,
        "vikram_name": get_samvat_name("vikram", vikram_year),
        "shaka_year": shaka_year,
        "shaka_name": get_samvat_name("shaka", shaka_year)
    }
    
    

def calculate_panchang(place: str, date: str):
    """
    Dynamically calculate the Panchang for a given place and date.
    Includes dynamic calculation of timings like Gulika Kaal, Rahu Kaal, etc.
    """
    try:
        # Fetch sun & moon rise/set times
        rise_set_data = get_sun_moon_rise_set(place, date)
        sunrise_str = rise_set_data.get("sun_rise", "N/A")
        sunset_str = rise_set_data.get("sun_set", "N/A")
        moonrise = rise_set_data.get("moon_rise", "N/A")
        moonset = rise_set_data.get("moon_set", "N/A")

        # Parse date object (for both panchang and for calculating weekday)
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        
        
        
        sun_times = get_panchang_timings(date_obj, place)
        

        # Parse timescale for astronomical calculations
        ts = load.timescale()
        t = ts.utc(date_obj.year, date_obj.month, date_obj.day)

        # Observer position (Earth)
        observer = earth

        # Get Samvat details (Vikram & Shaka)
        samvat = get_samvat_details(date_obj)

        # Calculate planetary positions
        sun_position = observer.at(t).observe(sun).apparent()
        moon_position = observer.at(t).observe(moon).apparent()

        sun_longitude = sun_position.ecliptic_latlon()[1].degrees
        moon_longitude = moon_position.ecliptic_latlon()[1].degrees

        # Lunar phase and tithi calculation
        lunar_phase = (moon_longitude - sun_longitude) % 360
        tithi_number = math.floor(lunar_phase / 12) + 1
        tithi_names = [
            "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami", "Shashthi", "Saptami", "Ashtami", 
            "Navami", "Dashami", "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Purnima",
            "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami", "Shashthi", "Saptami", "Ashtami", 
            "Navami", "Dashami", "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Amavasya"
        ]
        tithi = tithi_names[tithi_number - 1]

        # Nakshatra Calculation
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

        # Yoga Calculation
        sun_long_corrected = (sun_longitude - ayanamsa) % 360
        moon_long_corrected = (moon_longitude - ayanamsa) % 360
        yoga_angle = (sun_long_corrected + moon_long_corrected) % 360
        yoga_number = math.floor(yoga_angle / (13 + 20/60)) % 27
        yoga_names = [
            "Vishkumbha", "Priti", "Ayushman", "Saubhagya", "Shobhana", "Atiganda", "Sukarma", "Dhriti",
            "Shoola", "Ganda", "Vriddhi", "Dhruva", "Vyaghata", "Harshana", "Vajra", "Siddhi", "Vyatipata",
            "Variyana", "Parigha", "Shiva", "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma", "Indra", "Vaidhriti"
        ]
        yoga = yoga_names[yoga_number]

        # Karana Calculation
        karana_cycle = ["Bava", "Balava", "Kaulava", "Taitila", "Garaja", "Vanija", "Vishti"]
        fixed_karanas = ["Shakuni", "Chatushpada", "Naga", "Kimstughna"]

        if tithi_number in [30, 14]:
            karana = fixed_karanas[(tithi_number - 14) % 4]  # For last 4 fixed karanas
        else:
            karana_index = ((tithi_number - 1) * 2) % 7  # Dynamic karana calculation
            karana = karana_cycle[karana_index]

        paksha = "Shukla" if tithi_number <= 15 else "Krishna"

        # Dishashool (direction based on weekday; kept from your original mapping)
        dishashool_mapping = {
            "Monday": "East",
            "Tuesday": "North",
            "Wednesday": "North",
            "Thursday": "South",
            "Friday": "West",
            "Saturday": "East",
            "Sunday": "West"
        }
        dishashool = dishashool_mapping.get(date_obj.strftime('%A'), "Unknown")
        # Calculate special Panchang timings
        
        # Assemble final panchang details including dynamic timings
        panchang_details = {
            "sunrise": sunrise_str,
            "sunset": sunset_str,
            "moonrise": moonrise,
            "moonset": moonset,
            "date": date_obj.strftime('%d %B %Y'),
            "place": place,
            "tithi": tithi,
            "nakshatra": nakshatra,
            "yoga": yoga,
            "karana": karana,
            "paksha": paksha,
            "day": date_obj.strftime('%A'),
            "dishashool": dishashool,
            "samvat": {
                "shaka": f"{samvat['shaka_year']} {samvat['shaka_name']}",
                "vikram": f"{samvat['vikram_year']} {samvat['vikram_name']}"
            },
            "timings":sun_times 
        }
        return panchang_details

    except Exception as e:
        raise ValueError(f"Error in Panchang calculation: {str(e)}")


