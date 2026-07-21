from fastapi import APIRouter, HTTPException, Response

from src.schemas.users import UserRequestAdd, UserAdd, UserLogin
from src.services.auth import AuthService
from src.api.dependencies import UserIdDep, DBDep


router = APIRouter(prefix="/auth", tags=["Auth API"])


@router.post("/register")
async def register_user(
    data: UserRequestAdd,
    db: DBDep,
):
    try:
        hashed_password = AuthService().hash_password(data.password)
        new_user_data = UserAdd(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            hashed_password=hashed_password,
        )
    except:  # noqa
        raise HTTPException(status_code=400, detail="User exists")

    await db.users.add(new_user_data)
    await db.commit()

    return {"status": "Succesfully registered new user"}


@router.post("/login")
async def login_user(
    data: UserLogin,
    response: Response,
    db: DBDep,
):
    user = await db.users.get_user_with_hashed_pass(email=data.email)

    if not user:
        raise HTTPException(status_code=401, detail="Change your email")

    if not AuthService().verify_password(data.password, user.hashed_password):
        return HTTPException(status_code=401, detail="Password is incorrect")

    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)

    return {"access_token": access_token}


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: DBDep,
):
    await db.users.delete(id=user_id)
    await db.commit()

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
