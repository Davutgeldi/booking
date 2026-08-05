from datetime import date

from fastapi import APIRouter, Body
from fastapi import Query

from fastapi_cache.decorator import cache

from src.schemas.hotels import HotelPatch, HotelsAdd
from src.api.dependencies import PaginationDep, DBDep
from src.exceptions import check_date_to_after_date_from, ObjectNotFoundException, HotelNotFoundHTTPException
from src.services.hotels import HotelsService


router = APIRouter(prefix="/hotels", tags=["Hotels API"])


@router.get("")
@cache(expire=20)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description="Hotels title"),
    location: str | None = Query(None, description="Hotels location"),
):
    return await HotelsService(db).get_hotels(pagination=pagination, title=title, location=location)


@router.get("/available_hotels")
@cache(expire=20)
async def get_available_hotels(
    db: DBDep,
    title: str | None = None,
    location: str | None = None,
    limit: int = 10,
    offset: int = 0,
    date_from: date | None = Query(None, description="Check in date", example="2026-06-01"),
    date_to: date | None = Query(None, description="Check out date", example="2026-06-30"),
):
    check_date_to_after_date_from(date_from, date_to)
    return await HotelsService(db).get_available_hotels(
        date_from=date_from,
        date_to=date_to,
        title=title,
        location=location,
        limit=limit,
        offset=offset,
    )


@router.get("/{hotel_id}")
async def get_one_hotel(hotel_id: int, db: DBDep):
    try: 
        return await HotelsService(db).get_hotel(hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.post("")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelsAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Example 1",
                "value": {"title": "Hotel California", "location": "USA, California"},
            }
        }
    ),
):
    hotel = await HotelsService(db).add_hotel(hotel_data)

    return {"status": "Successfully added hotel", "data": hotel}


@router.put("/{hotel_id}")
async def edit_hotel(
    hotel_id: int,
    hotel_data: HotelsAdd,
    db: DBDep,
):
    await HotelsService(db).edit_hotel(hotel_id=hotel_id, hotel_data=hotel_data)

    return {"status": "Hotel successfully edited"}


@router.patch("/{hotel_id}")
async def partially_edit_hotel(
    hotel_id: int,
    hotel_data: HotelPatch,
    db: DBDep,
):
    await HotelsService(db).edit_hotel_partially(hotel_id=hotel_id, is_patch=True, hotel_data=hotel_data)


    return {"status": "Hotel successfully edited"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBDep):
    await HotelsService(db).delete_hotel(hotel_id=hotel_id)

    return {"status": "Hotel successfully deleted"}
