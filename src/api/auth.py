from fastapi import APIRouter, HTTPException, Response

from src.api.dependencies import UserIdDep
from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserAdd, UserRegister, UserLogin
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register", summary="Регистрация пользователя")
async def register_user(
    user_data: UserRegister,
):
    hashed_password = AuthService().hash_password(user_data.password)
    new_user_data = UserAdd(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        hashed_password=hashed_password,
    )
    async with async_session_maker() as session:
        res = await UsersRepository(session).add(new_user_data)
        await session.commit()

    return (
        {"status": "OK"}
        if res
        else HTTPException(
            status_code=401, detail="Пользователь с таким email уже зарегистрирован"
        )
    )


@router.post("/login", summary="Аутентификация пользователя")
async def login_user(
    user_data: UserLogin,
    response: Response,
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(
            email=user_data.email
        )
        if not user:
            raise HTTPException(
                status_code=401, detail="Пользователь с таким email не зарегистрирован"
            )
        if not AuthService().verify_password(user_data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Пароль неверный")

        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}

    return {"status": "OK"}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}


@router.get("/me")
async def get_me(user_id: UserIdDep):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
        return user
