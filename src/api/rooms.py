from datetime import date

from fastapi import APIRouter, Body, Query

from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomsAdd, RoomsPatch, RoomsAddRequest, RoomsPatchRequest
from src.api.dependencies import DBDep


router = APIRouter(prefix="/hotels", tags=["Rooms API"])


@router.get("/rooms/all")
async def get_all_rooms(
    pagination: PaginationDep,
    db: DBDep,
):
    per_page = pagination.per_page or 5
    return db.hotels.get_all(limit=per_page, offset=per_page * (pagination.page - 1))

@router.get("/{hotel_id}/rooms")
async def get_rooms(
    hotel_id: int, 
    db: DBDep,
    date_from: date = Query(None, description="Check in date", example="2026-06-01"),
    date_to: date = Query(None, description="Check out date", example="2026-06-30"),
):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)
    
@router.post("{hotel_id}/rooms")
async def create_room(
    db: DBDep,
    hotel_id: int,
    rooms_data: RoomsAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Example 1",
                "value": {
                    "title":"VIP room for celebrities",
                    "description": None,
                    "price": 69.99,
                    "quantity": 8,
                }
            } 
        }
    )
):
    _room_data = RoomsAdd(hotel_id=hotel_id, **rooms_data.model_dump())
    room = await db.rooms.add(_room_data)
    await db.commit()

    return {"status": "Successfully added room", "data": room}

@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_rooms(
    hotel_id: int,
    room_id: int,
    room_data: RoomsAddRequest,
    db: DBDep,
):
    _room_data = RoomsAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, id=room_id, hotel_id=hotel_id)
    await db.commit()

    return {"status": "Room successfully edited"}

@router.patch("/{hotel_id}/rooms/{room_id}")
async def partially_edit_room(
    hotel_id: int, 
    room_id: int,
    room_data: RoomsPatchRequest,
    db: DBDep,
):
    _room_data = RoomsPatch(hotel_id=hotel_id, **room_data.model_dump())

    await db.rooms.edit(_room_data, is_patch=True, id=room_id, hotel_id=hotel_id)
    await db.commit()

    return {"status": "Room successfully edited"}

@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(
    hotel_id: int,
    room_id: int,
    db: DBDep,
):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()

    return {"status": "Room successfully deleted"}