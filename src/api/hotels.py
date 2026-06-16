from datetime import date

from fastapi import APIRouter, Body
from fastapi import Query

from fastapi_cache.decorator import cache

from src.schemas.hotels import Hotels, HotelPatch, HotelsAdd
from src.api.dependencies import PaginationDep, DBDep
from src.database import async_session_maker
from src.repositories.hotels import HotelsRepository

router = APIRouter(prefix="/hotels", tags=["Hotels API"])


@router.get("")
@cache(expire=20)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description="Hotels title"),
    location: str | None = Query(None, description="Hotels location"),
):
    per_page = pagination.per_page or 10
    return await db.hotels.get_all(
        title=title,
        location=location,
        limit=per_page,
        offset=per_page * (pagination.page - 1),
    )

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
    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        title=title,
        location=location,
        limit=limit,
        offset=offset,
    )

@router.get("/{hotel_id}")
async def get_one_hotel(hotel_id: int, db: DBDep):
    hotel = await db.hotels.get_one_or_none(id=hotel_id)
    if hotel == None:
        return {"status": "Hotel doesn't exists"}
        
    return {"data": hotel}

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
    )
):  
    hotel = await db.hotels.add(hotel_data)
    await db.commit()

    return {"status": "Successfully added hotel", "data": hotel}


@router.put("/{hotel_id}")
async def edit_hotel(
    hotel_id: int,
    hotel_data: HotelsAdd,
    db: DBDep,
):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    
    return {"status": "Hotel successfully edited"}
    
@router.patch("/{hotel_id}")
async def partially_edit_hotel(
    hotel_id: int,
    hotel_data: HotelPatch,
    db: DBDep,
):
    await db.hotels.edit(hotel_data, is_patch=True, id=hotel_id)
    await db.commit()

    return {"status": "Hotel successfully edited"}

@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBDep):
    await db.hotels.delete(id=hotel_id)
    await db.commit()

    return {"status": "Hotel successfully deleted"}