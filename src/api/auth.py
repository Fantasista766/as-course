from fastapi import APIRouter

from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserAdd, UserRequestAdd

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register", summary="Регистрация пользователя")
async def register_user(
    user_data: UserRequestAdd,
):
    hashed_password = "13242fefaesf"
    new_user_data = UserAdd(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        hashed_password=hashed_password,
    )
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {"status": "OK"}
