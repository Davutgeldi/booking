from datetime import date

from fastapi import HTTPException


class BookingAppException(Exception):
    detail = "Catched error"

    def __init__(self, detail: str | None = None, *args, **kwargs):
        if detail:
            self.detail = detail

        super().__init__(self.detail, *args, **kwargs)


class BookingAppHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_to <= date_from:
        raise HTTPException(status_code=422, detail="The chenk in date cannot be later than check out date")


class ObjectNotFoundException(BookingAppException):
    detail = "Object not found"


class HotelNotFoundException(BookingAppException):
    detail = "Hotel not found"


class RoomNotFoundException(BookingAppException):
    detail = "Room not found"


class UserNotFoundException(BookingAppException):
    detail = "User not found"


class ObjectExistsException(BookingAppException):
    detail = "Object already exists"


class AllRoomsAreBookedException(BookingAppException):
    detail = "All rooms are already booked"


class UserAlreadyExistsException(BookingAppException):
    detail = "User with this email already exists"


class EmailNotRegisteredException(BookingAppException):
    detail = "Email is not registered"


class IncorrectPasswordException(BookingAppException):
    detail = "Password is incorrect"


class EmailNotRegisteredHTTPException(BookingAppHTTPException):
    status_code = 401
    detail = "Email is not registered"


class UserNotFoundHTTPException(BookingAppHTTPException):
    status_code = 404
    detail = "User not found"


class IncorrectPasswordHTTPException(BookingAppHTTPException):
    status_code = 401
    detail = "Password is incorrect"
    

class UserExistsHTTPException(BookingAppHTTPException):
    status_code = 409
    detail = "User with this email exists"


class HotelNotFoundHTTPException(BookingAppHTTPException):
    status_code = 404
    detail = "Hotel not found"


class RoomNotFoundHTTPException(BookingAppHTTPException):
    status_code = 404
    detail = "Room not found"