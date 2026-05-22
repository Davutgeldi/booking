from fastapi import APIRouter


router = APIRouter(prefix="/bookings", tags=["Bookings API"])


@router.post("")
async def create_booking():
    ...