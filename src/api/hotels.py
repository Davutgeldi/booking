from fastapi import APIRouter, Body

from sqlalchemy import insert, select, func
from fastapi import Query

from src.schemas.hotels import Hotels
from src.models.hotels import HotelsOrm
from src.api.dependencies import PaginationDep
from src.database import async_session_maker

router = APIRouter(prefix="/hotels")


@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(None, description="Hotels title"),
    location: str | None = Query(None, description="Hotels location")
):
    per_page = pagination.per_page or 10
    async with async_session_maker() as session:
        query = select(HotelsOrm)
        
        if title:
            query = query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))
        if location:
            query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))

        query = query.limit(per_page).offset(per_page * (pagination.page - 1))
        result = await session.execute(query)
        return result.scalars().all()


@router.post("")
async def create_hotel(
    hotel_data: Hotels = Body(
        openapi_examples={
            "1": {
                "summary": "Example 1",
                "value": {"title": "Hotel California", "location": "USA, California"},
            }
        }
    )
):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"status": "Successfully added hotel"}
