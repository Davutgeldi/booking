from fastapi import APIRouter, HTTPException, Response, Request

from src.schemas.users import UserRequestAdd, UserAdd, UserLogin
from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.services.auth import AuthService
from src.api.dependencies import UserIdDep


router = APIRouter(prefix="/auth", tags=["Auth API"])


@router.post("/register")
async def register_user(
    data: UserRequestAdd,
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        hashed_password=hashed_password,
    )
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {"status": "Succesfully registered new user"}


@router.post("/login")
async def login_user(
    data: UserLogin,
    response: Response,
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_pass(email=data.email)

        if not user:
            raise HTTPException(status_code=401, detail="Change your email")
        
        if not AuthService().verify_password(data.password, user.hashed_password):
            return HTTPException(status_code=401, detail="Password is incorrect")
        
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)

        return {"access_token": access_token}
    

@router.delete("/{user_id}")
async def delete_user(user_id: int):
    async with async_session_maker() as session:
        await UsersRepository(session).delete(id=user_id)
        await session.commit()
        return {"status": "User was succesfully deleted"}
    

@router.get("/me")
async def get_me(user_id: UserIdDep):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)

        return user


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")

    return {"status": "Successfully logged out"}