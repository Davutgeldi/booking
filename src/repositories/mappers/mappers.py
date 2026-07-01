from src.repositories.mappers.base import DataMapper

from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotels
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Rooms
from src.models.facilities import FacilitiesOrm
from src.schemas.facilities import Facility
from src.models.users import UsersOrm
from src.schemas.users import User


class HotelDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotels

class RoomDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = Rooms

class FacilityDataMapper(DataMapper):
    db_model = FacilitiesOrm
    schema = Facility

class UserDataMapper(DataMapper):
    db_model = UsersOrm
    schema = User