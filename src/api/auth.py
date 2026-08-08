from fastapi import APIRouter, HTTPException, Response

from src.schemas.users import UserRequestAdd, UserAdd, UserLogin
from src.services.auth import AuthService
from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import (
    UserAlreadyExistsException,
    UserExistsHTTPException,
    EmailNotRegisteredException,
    IncorrectPasswordException,
    EmailNotRegisteredHTTPException,
    IncorrectPasswordHTTPException,
    UserNotFoundException,
    UserNotFoundHTTPException,
)


router = APIRouter(prefix="/auth", tags=["Auth API"])


@router.post("/register")
async def register_user(
    data: UserRequestAdd,
    db: DBDep,
):
    try:
        await AuthService(db).register_user(data=data)
    except UserAlreadyExistsException:
        raise UserExistsHTTPException

    return {"status": "Succesfully registered new user"}


@router.post("/login")
async def login_user(
    data: UserLogin,
    response: Response,
    db: DBDep,
):
    try:
        access_token = await AuthService(db).login(data=data)
    except EmailNotRegisteredException:
        raise EmailNotRegisteredHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException
    
    response.set_cookie("access_token", access_token)

    return {"access_token": access_token}


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: DBDep,
):
    try:
        await AuthService(db).delete(user_id=user_id)
    except UserNotFoundException:
        raise UserNotFoundHTTPException

    return {"status": "User was succesfully deleted"}


@router.get("/me")
async def get_me(
    user_id: UserIdDep,
    db: DBDep,
):
    return await db.users.get_one_or_none(id=user_id)


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")

    return {"status": "Successfully logged out"}
