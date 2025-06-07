from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext
import jwt

from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserAdd, UserRequestAdd

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode |= {"exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/register", summary="Регистрация пользователя")
async def register_user(
    user_data: UserRequestAdd,
):
    hashed_password = pwd_context.hash(user_data.password)
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
        if not res
        else HTTPException(
            status_code=401, detail="Пользователь с таким email уже зарегистрирован"
        )
    )


@router.post("/login", summary="Аутентификация пользователя")
async def login_user(
    user_data: UserRequestAdd,
):
    # hashed_password = pwd_context.hash(user_data.password)
    # new_user_data = UserAdd(
    #     first_name=user_data.first_name,
    #     last_name=user_data.last_name,
    #     email=user_data.email,
    #     hashed_password=hashed_password,
    # )
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(email=user_data.email)
        if not user:
            raise HTTPException(
                status_code=401, detail="Пользователь с таким email не зарегистрирован"
            )
        access_token = create_access_token({"user_id": user.id})
        return {"access_token": access_token}

    return {"status": "OK"}
