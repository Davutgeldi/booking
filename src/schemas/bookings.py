from datetime import date

from pydantic import BaseModel


class BookingsAdd(BaseModel):
    user_id: int
    room_id: int
    date_from: date
    date_to: date
    price: float


class BookingsAddRequest(BaseModel):
    date_from: date
    date_to: date
    room_id: int


class Bookings(BookingsAdd):
    id: int
    