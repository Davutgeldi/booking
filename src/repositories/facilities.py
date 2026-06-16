from sqlalchemy import select, delete, insert

from src.repositories.base import BaseRepository
from src.schemas.facilities import Facility, RoomsFacility
from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facility


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomsFacility

    async def set_room_facilities(self, room_id: int, facility_ids: list[int]):
        get_current_facilities_ids = (
            select(self.model.facility_id)
            .filter_by(room_id=room_id)
        )

        result = await self.session.execute(get_current_facilities_ids)
        current_facilities_ids = result.scalars().all()

        ids_to_delete: list[int] = list(set(current_facilities_ids) - set(facility_ids))
        ids_to_insert: list[int] = list(set(facility_ids) - set(current_facilities_ids))

        if ids_to_delete:
            delete_m2m_facilities = (
                delete(self.model)
                .filter(
                    self.model.room_id == room_id,
                    self.model.facility_id.in_(ids_to_delete),
                )
            )
            await self.session.execute(delete_m2m_facilities)
        
        if ids_to_insert:
            insert_m2m_facilities = (
                insert(self.model)
                .values(
                    [{"room_id": room_id, "facility_id": facility_id} for facility_id in ids_to_insert]
                )
            )
            await self.session.execute(insert_m2m_facilities)
