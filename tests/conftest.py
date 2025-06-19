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
        print(f"{user_data=}")
