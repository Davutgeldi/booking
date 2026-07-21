from fastapi import APIRouter, HTTPException

from src.schemas.bookings import BookingsAddRequest, BookingsAdd, BookingsPatch
from src.api.dependencies import DBDep, UserIdDep


router = APIRouter(prefix="/bookings", tags=["Bookings API"])


@router.post("")
async def create_booking(
    user_id: UserIdDep,
    bookings_data: BookingsAddRequest,
    db: DBDep,
):
    room = await db.rooms.get_one_or_none(id=bookings_data.room_id)

    if room is None:
        raise HTTPException(
            status_code=404,
            detail="Room not found",
        )

    room_price = room.price
    _booking_data = BookingsAdd(
        user_id=user_id,
        price=room_price,
        **bookings_data.model_dump(),
    )

    booking = await db.bookings.add_booking(_booking_data, hotel_id=room.hotel_id)

    if booking is None:
        raise HTTPException(
            status_code=409,
            detail="Rooms are not available",
        )

    await db.commit()

    return {"status": "Successfully added", "data": booking}


@router.get("")
async def get_all_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me")
async def get_my_bookings(
    db: DBDep,
    user_id: UserIdDep,
):
    return await db.bookings.get_filtered(user_id=user_id)


@router.patch("/{booking_id}")
async def partially_edit_booking(
    booking_id: int,
    booking_data: BookingsPatch,
    db: DBDep,
):
    await db.bookings.edit(booking_data, is_patch=True, id=booking_id)
    await db.commit()

    return {"status": "Booking successfully edited"}


@router.put("/{booking_id}")
async def edit_booking(
    booking_id: int,
    booking_data: BookingsPatch,
    db: DBDep,
):
    await db.bookings.edit(booking_data, id=booking_id)
    await db.commit()

    return {"status": "Booking successfully edited"}
