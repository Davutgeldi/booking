from fastapi import APIRouter, Body

from fastapi import Query

from src.schemas.hotels import Hotels, HotelPatch, HotelsAdd
from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.repositories.hotels import HotelsRepository

router = APIRouter(prefix="/hotels")


@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(None, description="Hotels title"),
    location: str | None = Query(None, description="Hotels location")
):
    per_page = pagination.per_page or 10
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            title, 
            location,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )

@router.get("/{hotel_id}")
async def get_one_hotel(hotel_id: int):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).get_one_or_none(id=hotel_id)
        if hotel == None:
            return {"status": "Hotel doesn't exists"}
        
        return {"data": hotel}

@router.post("")
async def create_hotel(
    hotel_data: HotelsAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Example 1",
                "value": {"title": "Hotel California", "location": "USA, California"},
            }
        }
    )
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"status": "Successfully added hotel", "data": hotel}


@router.put("/{hotel_id}")
async def edit_hotel(
    hotel_id: int,
    hotel_data: HotelsAdd,
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()

        return {"status": "Hotel successfully edited"}
    
@router.patch("/{hotel_id}")
async def partially_edit_hotel(
    hotel_id: int,
    hotel_data: HotelPatch
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, is_patch=True, id=hotel_id)
        await session.commit()

        return {"status": "Hotel successfully edited"}

@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()

        return {"status": "Hotel successfully deleted"}