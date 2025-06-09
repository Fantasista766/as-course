from typing import Annotated

from fastapi import Depends, Query, HTTPException, Request
from pydantic import BaseModel

from src.database import async_session_maker
from src.repositories.hotels import HotelsRepository
from src.services.auth import AuthService


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


async def check_hotel_existence(hotel_id: int) -> int | None:
    """При PUT и PATCH номера сообщение как и при вставке, поэтому добавил в вывод hotel_id"""
    async with async_session_maker() as session:
        hotel_data = await HotelsRepository(session).get_one_or_none(id=hotel_id)
        if not hotel_data:
            raise HTTPException(
                status_code=404, detail=f"Отеля с id {hotel_id} нет в базе"
            )
        return hotel_data.id


HotelIdDep = Annotated[int, Depends(check_hotel_existence)]
