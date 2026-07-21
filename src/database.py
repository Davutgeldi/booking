from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import NullPool

from src.config import settings


# Alternative way to create engine with NullPool

# db_params = {}

# if settings.MODE == "TEST":
#     db_params = {"poolclass": NullPool}

# engine = create_async_engine(settings.DB_URL, echo=True, **db_params)

engine = create_async_engine(settings.DB_URL, echo=True)
engine_null_pool = create_async_engine(settings.DB_URL, poolclass=NullPool)

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)
async_session_maker_null_pool = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
