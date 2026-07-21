# ruff: noqa: E402
from typing import AsyncGenerator

import pytest
import json
from unittest import mock


mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start() 


from httpx import AsyncClient, ASGITransport 
from src.database import Base, engine_null_pool
from src.models import * 
from src.schemas.hotels import HotelsAdd
from src.schemas.rooms import RoomsAdd
from src.config import settings
from src.database import async_session_maker_null_pool
from src.api.dependencies import get_db
from src.main import app
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
async def check_test_mode():
    assert settings.MODE == "TEST"


async def get_db_null_pool():
    async with DBManager(async_session_maker_null_pool) as db:
        yield db


@pytest.fixture
async def db() -> AsyncGenerator[DBManager]: 
    async for db in get_db_null_pool():
        yield db


app.dependency_overrides[get_db] = get_db_null_pool

@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open("tests/mock_hotels.json", encoding="utf-8") as file_hotels:
        hotels = json.load(file_hotels)

    with open("tests/mock_rooms.json", encoding="utf-8") as file_rooms:
        rooms = json.load(file_rooms)

    hotels = [HotelsAdd.model_validate(hotel) for hotel in hotels]
    rooms = [RoomsAdd.model_validate(room) for room in rooms]

    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.hotels.add_bulk(hotels)
        await db_.rooms.add_bulk(rooms)
        await db_.commit()


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def register_user(ac, setup_database):
    await ac.post(
        "/auth/register",
        json={
            "first_name": "Didar",
            "last_name": "Yusubov",
            "email": "kabancik@gmail.com",
            "password": "qwerty123"
        }
    )


@pytest.fixture(scope="session")
async def authenticated_user(register_user, ac):
    await ac.post(
        "/auth/login",
        json={
            "email":"kabancik@gmail.com",
            "password": "qwerty123",
        }
    )

    assert ac.cookies["access_token"]

    yield ac