from pydantic import BaseModel

from src.schemas.facilities import Facility


class RoomsAddRequest(BaseModel):
    title: str
    description: str | None = None
    price: float
    quantity: int
    facilities_ids: list[int] = []


class RoomsAdd(BaseModel):
    hotel_id: int
    title: str
    description: str | None = None
    price: float
    quantity: int


class Rooms(RoomsAdd):
    id: int


class RoomWithRels(Rooms):
    facilities: list[Facility]


class RoomsPatchRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None
    quantity: int | None = None
    facilities_ids: list[int] = []


class RoomsPatch(BaseModel):
    hotel_id: int | None = None
    title: str | None = None
    description: str | None = None
    price: float | None = None
    quantity: int | None = None
