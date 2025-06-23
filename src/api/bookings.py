from datetime import datetime

from fastapi import APIRouter, HTTPException, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import AllRoomsAreBookedException, ObjectNotFoundException
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
    try:
        room_data = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=400, detail="Номер не найден")
    hotel_data = await db.hotels.get_one(id=room_data.hotel_id)
    _booking_data = BookingAddRequest(
        price=room_data.price,
        user_id=user_id,
        create_at=datetime.now(),
        **booking_data.model_dump(),
    )
    try:
        booking = await db.bookings.add_booking(_booking_data, hotel_data.id)
    except AllRoomsAreBookedException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)
    await db.commit()
    return {"status": "OK", "data": Booking.model_validate(booking)}
