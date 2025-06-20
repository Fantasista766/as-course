from datetime import date, datetime

from src.schemas.bookings import BookingAddRequest
from src.utils.db_manager import DBManager


async def test_add_booking(db: DBManager):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    create_at = datetime.now()
    booking_data = BookingAddRequest(
        user_id=user_id,  # type: ignore
        room_id=room_id,
        date_from=date(year=2025, month=12, day=12),
        date_to=date(year=2025, month=12, day=22),
        price=100,
        create_at=create_at,
    )
    await db.bookings.add(booking_data)
    await db.commit()
    new_booking_data = await db.bookings.get_all()
    assert new_booking_data[-1].user_id == user_id
    assert new_booking_data[-1].room_id == room_id
    assert new_booking_data[-1].date_from == date(year=2025, month=12, day=12)
    assert new_booking_data[-1].date_to == date(year=2025, month=12, day=22)
    assert new_booking_data[-1].price == 100
    assert new_booking_data[-1].create_at == create_at
