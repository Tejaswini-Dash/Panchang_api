
# def get_rahu_yamaganda(sun_times):
#     """
#     Compute Rahu Kaal and Yamaganda based on sunrise/sunset.
#     """
#     return {
#         "rahu_kaal": f"From {sun_times['rahu_start']} To {sun_times['rahu_end']}",
#         "yamaganda": f"From {sun_times['yamaganda_start']} To {sun_times['yamaganda_end']}"
#     }


def get_rahu_yamaganda(sun_times):
    """
    Extract Rahu Kaal and Yamaganda timings from computed sun times.
    """
    return {
        "rahu_kaal": sun_times["rahu_kaal"],
        "yamaganda": sun_times["yamaganda"]
    }
