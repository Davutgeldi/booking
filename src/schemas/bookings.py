from datetime import date

from pydantic import BaseModel, Field


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
    

class BookingsPatch(BaseModel):
    room_id: int | None = Field(default=None, description="Room ID")
    date_from: date | None = Field(default=None, description="Date from")
    date_to: date | None = Field(default=None, description="Date to")
    price: float | None = Field(default=None, description="Price of the booking")