from typing import Any, AsyncGenerator, Callable
from unittest import mock
import json

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()  # type: ignore

from httpx import AsyncClient, ASGITransport
import pytest

from src.api.dependencies import get_db
from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.main import app
from src.models import *
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
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

    hotels_models = [HotelAdd.model_validate(hotel) for hotel in hotels]
    rooms_models = [RoomAdd.model_validate(room) for room in rooms]

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
    user_data = await ac.post(
        "/auth/register",
        json={
            "email": "kot@pes.com",
            "password": "1234",
            "first_name": "A",
            "last_name": "B",
        },
    )
    assert user_data.status_code == 200


@pytest.fixture(scope="session", autouse=True)
async def authenticated_ac(register_user: Callable[..., Any], ac: AsyncClient):
    await ac.post(
        "/auth/login",
        json={
            "email": "kot@pes.com",
            "password": "1234",
        },
    )
    assert "access_token" in ac.cookies
    yield ac
