from typing import Annotated

from fastapi import Depends, Query, Request
from pydantic import BaseModel

from src.database import async_session_maker
from src.exceptions import JWTMissingException, JWTMissingHTTPException
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


async def get_token(request: Request) -> str:
    try:
        return AuthService().get_token(request)
    except JWTMissingException:
        raise JWTMissingHTTPException


async def get_current_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService().decode_token(token)
    return data["user_id"]


UserIdDep = Annotated[int, Depends(get_current_user_id)]


def get_db_manager():
    return DBManager(session_factory=async_session_maker)


async def get_db():
    async with get_db_manager() as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
