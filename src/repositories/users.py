from sqlalchemy import select
from pydantic import EmailStr

from src.repositories.base import BaseRepository
from src.models.users import UsersOrm
from src.schemas.users import UserWithHashedPass
from src.repositories.mappers.mappers import UserDataMapper


class UsersRepository(BaseRepository):
    model = UsersOrm
    mapper = UserDataMapper

    async def get_user_with_hashed_pass(self, email: EmailStr):
        query = select(UsersOrm).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one()

        return UserWithHashedPass.model_validate(model, from_attributes=True)
