from typing import Any, Callable

from httpx import AsyncClient
import pytest

from src.utils.db_manager import DBManager


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (1, "2025-06-21", "2025-06-28", 200),
        (1, "2025-06-22", "2025-06-29", 200),
        (1, "2025-06-23", "2025-06-30", 200),
        (1, "2025-06-24", "2025-07-01", 200),
        (1, "2025-06-25", "2025-07-02", 200),
        (1, "2025-06-26", "2025-07-03", 404),
        (1, "2025-07-25", "2025-07-26", 200),
    ],
)
async def test_add_booking(
    room_id: int,
    date_from: str,
    date_to: str,
    status_code: int,
    authenticated_ac: AsyncClient,
):
    response = await authenticated_ac.post(
        "/bookings",
        json={"room_id": room_id, "date_from": date_from, "date_to": date_to},
    )
    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "OK"
        assert res["data"]["room_id"] == room_id


@pytest.fixture(scope="module")
async def delete_all_bookings(db_module: DBManager, authenticated_ac: AsyncClient):
    response = await authenticated_ac.get("/auth/me")
    user_id = response.json()["id"]
    response = await db_module.bookings.get_filtered(user_id=user_id)
    ids_to_delete = [booking.id for booking in response]
    await db_module.bookings.delete_batch_by_ids(ids_to_delete=ids_to_delete)
    await db_module.commit()


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code, bookings_amount",
    [
        (1, "2025-06-21", "2025-06-28", 200, 1),
        (1, "2025-06-22", "2025-06-29", 200, 2),
        (1, "2025-06-23", "2025-06-30", 200, 3),
    ],
)
async def test_add_and_get_my_bookings(
    room_id: int,
    date_from: str,
    date_to: str,
    status_code: int,
    bookings_amount: int,
    authenticated_ac: AsyncClient,
    delete_all_bookings: Callable[..., Any],
):
    # добавили бронь
    response = await authenticated_ac.post(
        "/bookings",
        json={"room_id": room_id, "date_from": date_from, "date_to": date_to},
    )
    assert response.status_code == status_code

    response = await authenticated_ac.get("/bookings/me")
    assert response.status_code == status_code
    assert len(response.json()) == bookings_amount
