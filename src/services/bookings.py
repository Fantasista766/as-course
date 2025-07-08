from datetime import datetime

from src.exceptions import (
    AllRoomsAreBookedException,
    AllRoomsAreBookedHTTPException,
)
from src.schemas.bookings import Booking, BookingAdd, BookingAddRequest
from src.services.base import BaseService
from src.services.hotels import HotelService
from src.services.rooms import RoomService


class BookingService(BaseService):
    async def get_all_bookings(self) -> list[Booking]:
        return await self.db.bookings.get_all()  # type: ignore

    async def get_user_bookings(self, user_id: int) -> list[Booking]:
        return await self.db.bookings.get_filtered(user_id=user_id)  # type: ignore

    async def add_booking(self, user_id: int, booking_data: BookingAdd) -> Booking:
        room_data = await RoomService(self.db).get_room_with_check(booking_data.room_id)
        hotel_data = await HotelService(self.db).get_hotel_with_check(room_data.hotel_id)
        _booking_data = BookingAddRequest(
            price=room_data.price,
            user_id=user_id,
            create_at=datetime.now(),
            **booking_data.model_dump(),
        )
        try:
            booking = await self.db.bookings.add_booking(_booking_data, hotel_data.id)  # type: ignore
            await self.db.commit()  # type: ignore
            return booking
        except AllRoomsAreBookedException:
            raise AllRoomsAreBookedHTTPException
