<<<<<<< HEAD
# from fastapi import APIRouter, HTTPException
# from fastapi.responses import JSONResponse
# from pydantic import BaseModel
# from ..services.panchang_service import get_panchang_for_date

# router = APIRouter()

# # Request Body Model
# class PanchangRequest(BaseModel):
#     place: str
#     date: str  # Expected format: YYYY-MM-DD

# @router.post("/panchang")
# async def get_panchang(request: PanchangRequest):
#     """
#     Route to calculate Panchang for a given place and date.
#     """
#     try:
#         panchang = get_panchang_for_date(request.place, request.date)
#         return JSONResponse(content=panchang)
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))




from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from ..services.panchang_service import get_panchang_for_date

router = APIRouter()

# Request Body Model
class PanchangRequest(BaseModel):
    place: str
    date: str  # Expected format: YYYY-MM-DD

@router.post("/panchang")
async def get_panchang(request: PanchangRequest):
    """
    Route to calculate Panchang for a given place and date.
    """
    try:
        panchang = get_panchang_for_date(request.place, request.date)
        return JSONResponse(content=panchang)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
=======
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

>>>>>>> b8a42b75d440e17b91f20f3edc6ef857bd7e3483
