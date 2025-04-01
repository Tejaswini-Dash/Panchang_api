# def get_rahu_yamaganda(sun_times):
#     """
#     Compute Rahu Kaal and Yamaganda timings based on sunrise/sunset.
#     """
#     # Placeholder logic for Rahu Kaal and Yamaganda (use precise calculations)
#     return {
#         "rahu_kaal": "10:30 AM - 12:00 PM",
#         "yamaganda": "3:00 PM - 4:30 PM"
#     }


def get_rahu_yamaganda(sun_times):
    """
    Compute Rahu Kaal and Yamaganda based on sunrise/sunset.
    """
    return {
        "rahu_kaal": f"From {sun_times['rahu_start']} To {sun_times['rahu_end']}",
        "yamaganda": f"From {sun_times['yamaganda_start']} To {sun_times['yamaganda_end']}"
    }
