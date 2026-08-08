from datetime import datetime, timezone, timedelta

from passlib.context import CryptContext
import jwt
from fastapi import HTTPException

from src.config import settings
from src.services.base import BaseService
from src.schemas.users import UserRequestAdd, UserAdd, UserLogin
from src.exceptions import (
    ObjectNotFoundException,
    ObjectExistsException, 
    UserNotFoundException,
    UserAlreadyExistsException,
    EmailNotRegisteredException,
    IncorrectPasswordException,
)


ACCESS_TOKEN_EXPIRE_MINUTES = 30


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )

        return encoded_jwt

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def decode_token(self, token: str) -> str:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=settings.JWT_ALGORITHM)
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code=401, detail="Incorrect authentication data")

    async def register_user(self, data: UserRequestAdd):
        hashed_password = AuthService().hash_password(data.password)
        new_user_data = UserAdd(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            hashed_password=hashed_password,
        )

        try:
            await self.db.users.add(new_user_data)
            await self.db.commit()
        except ObjectExistsException:
            raise UserAlreadyExistsException

    async def login(self, data: UserLogin):
        user = await self.db.users.get_user_with_hashed_pass(email=data.email)

        if not user:
            raise EmailNotRegisteredException

        if not self.verify_password(data.password, user.hashed_password):
            raise IncorrectPasswordException

        access_token = AuthService().create_access_token({"user_id": user.id})

        return access_token

    async def delete(self, user_id: int):
        try:
            await self.db.users.get_one(id=user_id)
        except ObjectNotFoundException:
            raise UserNotFoundException

        await self.db.users.delete(id=user_id)
        await self.db.commit()

    async def get_one(self, user_id: int):
        try:
            return await self.db.users.get_one(id=user_id)
        except ObjectNotFoundException:
            raise UserNotFoundException
