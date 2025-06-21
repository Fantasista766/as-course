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
    db: DBManager,
    authenticated_ac: AsyncClient,
):
    # room_id = (await db.rooms.get_all())[0].id
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
