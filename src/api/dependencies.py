from typing import Annotated

from fastapi import Depends, Query, HTTPException, Request
from pydantic import BaseModel

from src.database import async_session_maker
from src.services.auth import AuthService
from src.utils.db_manager import DBManager


class PaginationParams(BaseModel):
    page: Annotated[
        int | None,
        Query(1, ge=1, description="Номер страницы"),
    ]
    per_page: Annotated[
        int | None,
        Query(None, ge=1, lt=100, description="Количество отелей на странице"),
    ]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request) -> str:
    token = request.cookies.get("access_token", "")
    if not token:
        raise HTTPException(status_code=401, detail="Вы не предоставили токен доступа")
    return token


def get_current_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService().decode_token(token)
    return data["user_id"]


UserIdDep = Annotated[int, Depends(get_current_user_id)]


def get_db_manager():
    return DBManager(session_factory=async_session_maker)


async def get_db():
    async with get_db_manager() as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]


async def check_hotel_existence(db: DBDep, hotel_id: int) -> int | None:
    """При PUT и PATCH номера сообщение как и при вставке, поэтому добавил в вывод hotel_id"""
    hotel_data = await db.hotels.get_one_or_none(id=hotel_id)
    if not hotel_data:
        raise HTTPException(status_code=404, detail=f"Отеля с id {hotel_id} нет в базе")
    return hotel_data.id


HotelIdDep = Annotated[int, Depends(check_hotel_existence)]
