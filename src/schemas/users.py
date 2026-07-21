from pydantic import BaseModel, EmailStr


class UserRequestAdd(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr
    password: str


class UserAdd(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr
    hashed_password: str


class User(BaseModel):
    id: int
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserWithHashedPass(BaseModel):
    id: int
    email: EmailStr
    hashed_password: str
