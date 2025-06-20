import json

from httpx import AsyncClient, ASGITransport
import pytest

from src.config import settings
from src.database import Base, engine_null_pool
from src.main import app
from src.models import *


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):  # type: ignore
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def load_data_to_db(setup_database):  # type: ignore
    with open("tests/mock_hotels.json", "r") as f:
        hotels = json.load(f)

    with open("tests/mock_rooms.json", "r") as f:
        rooms = json.load(f)

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test", follow_redirects=True
    ) as ac:
        for hotel in hotels:
            hotel_data = await ac.post("/hotels", json=hotel)
            assert hotel_data.status_code == 200
        for room in rooms:
            room_data = await ac.post(
                f"/hotels/{room['hotel_id']}/rooms",
                json=room,
            )
            assert room_data.status_code == 200


@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database):  # type: ignore
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
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
