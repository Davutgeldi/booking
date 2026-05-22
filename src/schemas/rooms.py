from pydantic import BaseModel



class RoomsAddRequest(BaseModel):
    title: str 
    description: str | None = None
    price: float
    quantity: int


class RoomsAdd(BaseModel):
    hotel_id: int
    title: str
    description: str | None = None
    price: float
    quantity: int


class Rooms(RoomsAdd):
    id: int


class RoomsPatchRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None
    quantity: int | None = None


class RoomsPatch(BaseModel):
    hotel_id: int | None = None
    title: str | None = None
    description: str | None = None
    price: float | None = None
    quantity: int | None = None