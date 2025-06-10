from fastapi import APIRouter, HTTPException, Body

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import Booking, BookingAdd, BookingAddRequest

router = APIRouter(prefix="/bookings", tags=["Брони"])


@router.post(
    "/",
    summary="Создать новую бронь",
)
async def create_booking(
    db: DBDep, user_id: UserIdDep, booking_data: BookingAdd = Body()
) -> dict[str, str | Booking]:
    room_data = await db.rooms.get_one_or_none(id=booking_data.room_id)
    if not room_data:
        raise HTTPException(
            status_code=404, detail=f"Номера с id {booking_data.room_id} нет в базе"
        )

    _booking_data = BookingAddRequest(
        room_id=booking_data.room_id,
        date_from=booking_data.date_from,
        date_to=booking_data.date_to,
        price=room_data.price,
        user_id=user_id,
    )

    booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "OK", "data": Booking.model_validate(booking)}
