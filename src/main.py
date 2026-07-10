from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.backends.inmemory import InMemoryBackend


import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.setup import redis_manager
from src.api.hotels import router as router_hotels
from src.api.auth import router as router_auth
from src.api.rooms import router as router_rooms
from src.api.bookings import router as router_bookings
from src.api.facilities import router as router_facilities
from src.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()
    yield 
    await redis_manager.close()

#can use this in test mode, redis for test
# if settings.MODE == "TEST":
#     FastAPICache.init(InMemoryBackend(), prefix="")

app = FastAPI(title="Hotels Booking")

app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)
app.include_router(router_facilities)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
