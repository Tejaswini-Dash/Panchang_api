# from fastapi import APIRouter, Query
# from datetime import date
# from app.services.panchang_service import compute_panchang

# router = APIRouter()

# @router.get("/panchang")
# async def get_panchang(
#     location: str = Query(..., description="City name or latitude,longitude"),
#     date_value: date = Query(..., description="Date for Panchang calculation")
# ):
#     """
#     Get Panchang details for a given date and location.
#     """
#     return compute_panchang(location, date_value)



from fastapi import APIRouter, Query
from datetime import date
from app.services.panchang_service import compute_panchang

router = APIRouter()

@router.get("/panchang")
async def get_panchang(
    location: str = Query(..., description="City name or latitude,longitude"),
    date_value: date = Query(..., description="Date for Panchang calculation")
):
    """
    Get detailed Panchang for a given date and location.
    """
    return compute_panchang(location, date_value)

