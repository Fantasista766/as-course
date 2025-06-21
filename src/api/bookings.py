from datetime import datetime

from fastapi import APIRouter, HTTPException, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import Booking, BookingAdd, BookingAddRequest

router = APIRouter(prefix="/bookings", tags=["Брони"])


@router.get("/", summary="Получить список бронирований")
@cache(expire=10)
async def get_bookings(db: DBDep) -> list[Booking]:
    return await db.bookings.get_all()


@router.get("/me", summary="Получить список бронирований пользователя")
@cache(expire=10)
async def get_user_bookings(db: DBDep, user_id: UserIdDep) -> list[Booking]:
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("/", summary="Создать новую бронь")
async def create_booking(
    db: DBDep,
    user_id: UserIdDep,
    booking_data: BookingAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Бронь 1",
                "value": {
                    "room_id": 1,
                    "date_from": "2025-06-10",
                    "date_to": "2025-06-20",
                },
            },
        }
    ),
) -> dict[str, str | Booking]:
    room_data = await db.rooms.get_one_or_none(id=booking_data.room_id)
    if not room_data:
        raise HTTPException(
            status_code=404, detail=f"Номера с id {booking_data.room_id} нет в базе"
        )

    _booking_data = BookingAddRequest(
        price=room_data.price,
        user_id=user_id,
        create_at=datetime.now(),
        **booking_data.model_dump(),
    )
    try:
        booking = await db.bookings.add_booking(_booking_data)
        await db.commit()
    except Exception:
        raise HTTPException(status_code=404, detail="Нет свободных номеров на эти даты")
    return {"status": "OK", "data": Booking.model_validate(booking)}
