from datetime import date, datetime

from src.schemas.bookings import BookingAddRequest
from src.utils.db_manager import DBManager


async def test_booking_crud(db: DBManager):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    create_at = datetime.now()

    create_date_from = date(year=2025, month=12, day=12)
    create_date_to = date(year=2025, month=12, day=22)

    # create data
    booking_data = BookingAddRequest(
        user_id=user_id,  # type: ignore
        room_id=room_id,
        date_from=create_date_from,
        date_to=create_date_to,
        price=100,  # type: ignore
        create_at=create_at,  # type: ignore
    )
    new_booking = await db.bookings.add(booking_data)

    # read data
    read_booking_data = await db.bookings.get_one_or_none(id=new_booking.id)
    assert read_booking_data.user_id == user_id
    assert read_booking_data.room_id == room_id
    assert read_booking_data.date_from == create_date_from
    assert read_booking_data.date_to == create_date_to
    assert read_booking_data.price == 100
    assert read_booking_data.create_at == create_at

    # update data
    update_booking_data = BookingAddRequest(
        user_id=user_id,  # type: ignore
        room_id=room_id,
        date_from=date(year=2026, month=1, day=12),
        date_to=date(year=2026, month=1, day=22),
        price=100,  # type: ignore
    )
    await db.bookings.edit(update_booking_data, exclude_unset=True, id=read_booking_data.id)

    # delete data
    await db.bookings.delete(id=read_booking_data.id)
    await db.commit()
