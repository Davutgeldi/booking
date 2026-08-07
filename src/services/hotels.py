from datetime import date

from src.exceptions import check_date_to_after_date_from, HotelNotFoundException, ObjectNotFoundException
from src.schemas.hotels import HotelsAdd, HotelPatch, Hotels
from src.services.base import BaseService
from src.api.dependencies import PaginationDep


class HotelsService(BaseService):
    async def get_hotels(
            self,
            pagination: PaginationDep,
            title: str | None = None, 
            location: str | None = None,
    ):
        per_page = pagination.per_page or 10
        return await self.db.hotels.get_all(
            title=title,
            location=location,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )

    async def get_available_hotels(
            self,
            date_from: date | None = None,
            date_to: date | None = None,
            title: str | None = None,
            location: str | None = None,
            limit: int = 10,
            offset: int = 0,
    ):
        check_date_to_after_date_from(date_from, date_to)
        return await self.db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            title=title,
            location=location,
            limit=limit,
            offset=offset,
        )

    async def get_hotel_with_check(
            self, 
            hotel_id: int,
    ) -> Hotels:
        try:
            return await self.get_hotel(hotel_id=hotel_id)
        except ObjectNotFoundException as ex:
            raise HotelNotFoundException from ex

    async def get_hotel(self, hotel_id: int):
        return await self.db.hotels.get_one(id=hotel_id)

    async def add_hotel(self, hotel_data: HotelsAdd):
        hotel = await self.db.hotels.add(hotel_data)
        await self.db.commit()

        return hotel

    async def edit_hotel(self, hotel_id: int, hotel_data: HotelPatch):
        hotel = await self.db.hotels.edit(hotel_data, id=hotel_id)
        await self.db.commit()

        return hotel
    
    async def edit_hotel_partially(self, hotel_id: int, hotel_data: HotelPatch):
        hotel = await self.db.hotels.edit(hotel_data, is_patch=True, id=hotel_id)
        await self.db.commit()

        return hotel

    async def delete_hotel(self, hotel_id: int):
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()
