from datetime import date

from src.exceptions import (
    check_date_to_after_date_from,
    ObjectNotFoundException,
    HotelNotFoundException,
    RoomNotFoundException,
)
from src.api.dependencies import PaginationDep
from src.schemas.facilities import RoomsFacilityAdd
from src.schemas.rooms import RoomsAddRequest, Rooms, RoomsAdd, RoomsPatchRequest, RoomsPatch
from src.services.base import BaseService
from src.services.hotels import HotelsService


class RoomsService(BaseService):
    async def get_all(
            self,
            pagination: PaginationDep,
    ):
        per_page = pagination.per_page or 5
        return await self.db.rooms.get_all(per_page=per_page, offset=per_page * (pagination.page - 1))

    async def get_rooms(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date,
    ):
        check_date_to_after_date_from(date_from, date_to)
        return await self.db.rooms.get_filtered_by_time(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )

    async def get_one_room(self, hotel_id: int, room_id: int):
        room = await self.db.rooms.get_one_or_none_with_rels(id=room_id, hotel_id=hotel_id)

        if not room:
            raise RoomNotFoundException

        return room

    async def add_room(
            self,
            hotel_id: int,
            rooms_data: RoomsAddRequest,
    ):
        try:
            hotel = await HotelsService(self.db).get_hotel(hotel_id=hotel_id)

        except ObjectNotFoundException as ex:
            raise HotelNotFoundException from ex
        
        _room_data = RoomsAdd(hotel_id=hotel_id, **rooms_data.model_dump())
        room = await self.db.rooms.add(_room_data)
        rooms_facilities_data = [
            RoomsFacilityAdd(room_id=room.id, facility_id=facility_id) for facility_id in rooms_data.facilities_ids
        ]
        await self.db.rooms_facilities.add_bulk(rooms_facilities_data)
        await self.db.commit()

        return room

    async def edit_room(
            self,
            hotel_id: int, 
            room_id: int,
            room_data: RoomsPatchRequest,
    ):
        try:
            await HotelsService(self.db).get_hotel_with_check(hotel_id=hotel_id)
        except ObjectNotFoundException as ex:
            raise HotelNotFoundException from ex

        try:
            await self.db.rooms.get_one(id=room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException
            
        _room_data = RoomsAdd(hotel_id=hotel_id, **room_data.model_dump())
        await self.db.rooms.edit(_room_data, id=room_id, hotel_id=hotel_id)
        await self.db.rooms_facilities.set_room_facilities(room_id, room_data.facilities_ids)
        await self.db.commit()

    async def edit_room_partially(
            self,
            hotel_id: int,
            room_id: int,
            room_data: RoomsPatchRequest,
    ):
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException

        try:
            await self.db.rooms.get_one(id=room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException
    
        _room_data_dict = room_data.model_dump(exclude_unset=True)
        _room_data = RoomsPatch(hotel_id=hotel_id, **_room_data_dict)

        if "facilities_ids" in _room_data_dict:
            await self.db.rooms_facilities.set_room_facilities(room_id, _room_data_dict["facilities_ids"])

        await self.db.rooms.edit(_room_data, is_patch=True, id=room_id, hotel_id=hotel_id)
        await self.db.commit()

    async def delete(
            self,
            hotel_id: int,
            room_id: int,
    ):
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException: 
            raise HotelNotFoundException
    
        try:
            await self.db.rooms.get_one(id=room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException
    
        await self.db.rooms.delete(id=room_id, hotel_id=hotel_id)
        await self.db.commit()

    async def get_room_with_check(self, room_id: int) -> Rooms:        
        try:            
            return await self.db.rooms.get_one(id=room_id)        
        except ObjectNotFoundException:            
            raise RoomNotFoundException
