from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import (
    AllRoomsAreBookedException,
    AllRoomsAreBookedHTTPException,
)
from src.schemas.bookings import Booking, BookingAdd
from src.services.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["Брони"])


@router.get("/", summary="Получить список бронирований")
@cache(expire=10)
async def get_bookings(db: DBDep) -> list[Booking]:
    return await BookingService(db).get_all_bookings()


@router.get("/me", summary="Получить список бронирований пользователя")
@cache(expire=10)
async def get_user_bookings(db: DBDep, user_id: UserIdDep) -> list[Booking]:
    return await BookingService(db).get_user_bookings(user_id)


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
        booking = await BookingService(db).add_booking(user_id, booking_data)
        return {"status": "OK", "data": Booking.model_validate(booking)}
    except AllRoomsAreBookedException:
        raise AllRoomsAreBookedHTTPException
