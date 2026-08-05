from contextlib import asynccontextmanager
import logging
import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi_cache import FastAPICache  # noqa
from fastapi_cache.backends.redis import RedisBackend  # noqa
from fastapi_cache.backends.inmemory import InMemoryBackend  # noqa
import uvicorn


sys.path.append(str(Path(__file__).parent.parent))

logging.basicConfig(level=logging.DEBUG)

from src.setup import redis_manager
from src.api.hotels import router as router_hotels
from src.api.auth import router as router_auth
from src.api.rooms import router as router_rooms
from src.api.bookings import router as router_bookings
from src.api.facilities import router as router_facilities


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
    yield
    await redis_manager.close()


# can use this in test mode, redis for test
# if settings.MODE == "TEST":
#     FastAPICache.init(InMemoryBackend(), prefix="")
#     logging.info("Using InMemoryBackend for caching")

app = FastAPI(title="Hotels Booking", lifespan=lifespan)

app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)
app.include_router(router_facilities)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
