from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from ..services.service import get_panchang_for_date

router = APIRouter()

# Request Body Model
class PanchangRequest(BaseModel):
    date: str  # Expected format: YYYY-MM-DD
    place: str

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
