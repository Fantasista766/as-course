# ruff: noqa: E402, F403
from typing import Any, AsyncGenerator, Callable
from unittest import mock
import json

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

from httpx import AsyncClient, ASGITransport
import pytest

from src.api.dependencies import get_db
from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.main import app
from src.models import *
from src.schemas.hotels import HotelAddDTO
from src.schemas.rooms import RoomAddDTO
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


async def get_db_null_pool() -> AsyncGenerator[DBManager, Any]:
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="function")
async def db() -> Any:
    async for db in get_db_null_pool():
        yield db


@pytest.fixture(scope="module")
async def db_module() -> Any:
    async for db_module in get_db_null_pool():
        yield db_module


app.dependency_overrides[get_db] = get_db_null_pool


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode: Callable[..., Any]):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def load_data_to_db(setup_database: Callable[..., Any]):
    with open("tests/mock_hotels.json", "r") as f:
        hotels = json.load(f)

    with open("tests/mock_rooms.json", "r") as f:
        rooms = json.load(f)

    hotels_models = [HotelAddDTO.model_validate(hotel) for hotel in hotels]
    rooms_models = [RoomAddDTO.model_validate(room) for room in rooms]

    async with DBManager(session_factory=async_session_maker_null_pool) as _db:
        await _db.hotels.add_batch(hotels_models)
        await _db.rooms.add_batch(rooms_models)
        await _db.commit()


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, Any]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test", follow_redirects=True
    ) as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database: Callable[..., Any], ac: AsyncClient):
    response = await ac.post(
        "/auth/register",
        json={
            "email": "kot@pes.com",
            "password": "12341234",
            "first_name": "Alan",
            "last_name": "Beber",
        },
    )
    assert response.status_code == 200


@pytest.fixture(scope="session")
async def authenticated_ac(register_user: Callable[..., Any], ac: AsyncClient):
    await ac.post(
        "/auth/login",
        json={
            "email": "kot@pes.com",
            "password": "12341234",
        },
    )
    assert "access_token" in ac.cookies
    yield ac
