from src.schemas.hotels import HotelsAdd
from src.utils.db_manager import DBManager
from src.database import async_session_maker_null_pool
from src.config import settings


async def test_add_hotel(db):
    hotel_data = HotelsAdd(title="Hotel 5 stars", location="Sochi")

    new_hotel = await db.hotels.add(hotel_data)
    await db.commit()
    print(new_hotel)