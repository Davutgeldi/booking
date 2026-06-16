from src.repositories.mappers.base import DataMapper

from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotels
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Rooms


class HotelDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotels

class RoomDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = Rooms