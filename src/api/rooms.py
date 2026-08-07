from datetime import date

from fastapi import APIRouter, Body, Query

from src.api.dependencies import PaginationDep
from src.schemas.rooms import RoomsAdd, RoomsPatch, RoomsAddRequest, RoomsPatchRequest
from src.schemas.facilities import RoomsFacilityAdd
from src.api.dependencies import DBDep
from src.services.rooms import RoomsService
from src.exceptions import (
    RoomNotFoundException,
    RoomNotFoundHTTPException,
    HotelNotFoundException,
)
from src.exceptions import (
    check_date_to_after_date_from,
    ObjectNotFoundException,
    HotelNotFoundHTTPException,
    RoomNotFoundHTTPException
)


router = APIRouter(prefix="/hotels", tags=["Rooms API"])


@router.get("/rooms/all")
async def get_all_rooms(
    pagination: PaginationDep,
    db: DBDep,
):
    return await RoomsService(db).get_all(pagination=pagination)


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(None, description="Check in date", example="2026-06-01"),
    date_to: date = Query(None, description="Check out date", example="2026-06-30"),
):
    return await RoomsService(db).get_rooms(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_one_room(
    hotel_id: int,
    room_id: int,
    db: DBDep,
):
    try:
        return await RoomsService(db).get_one_room(hotel_id=hotel_id, room_id=room_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


@router.post("/{hotel_id}/rooms")
async def create_room(
    db: DBDep,
    hotel_id: int,
    rooms_data: RoomsAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Example 1",
                "value": {
                    "title": "VIP room for celebrities",
                    "description": None,
                    "price": 69.99,
                    "quantity": 8,
                    "facilities_ids": [1, 2],
                },
            }
        }
    ),
):
    try:
        room = await RoomsService(db).add_room(hotel_id=hotel_id, rooms_data=rooms_data)
    except HotelNotFoundException as ex:
        raise HotelNotFoundHTTPException from ex

    return {"status": "Successfully added room", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_rooms(
    hotel_id: int,
    room_id: int,
    room_data: RoomsAddRequest,
    db: DBDep,
):
    try:
        await RoomsService(db).edit_room(hotel_id=hotel_id, room_id=room_id, room_data=room_data)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException

    return {"status": "Room successfully edited"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def partially_edit_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomsPatchRequest,
    db: DBDep,
):
    try:
        await RoomsService(db).edit_room_partially(hotel_id=hotel_id, room_id=room_id, room_data=room_data)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException

    return {"status": "Room successfully edited"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(
    hotel_id: int,
    room_id: int,
    db: DBDep,
):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException: 
        raise HotelNotFoundHTTPException
    
    try:
        await db.rooms.get_one(id=room_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException
    
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()

    return {"status": "Room successfully deleted"}
