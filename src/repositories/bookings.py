from datetime import date

from sqlalchemy import select

from src.exceptions import AllRoomsAreBookedException
from src.models.bookings import BookingsORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.bookings import BookingAddRequest


class BookingsRepository(BaseRepository):
    model = BookingsORM
    mapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        query = select(self.model).filter(self.model.date_from == date.today())
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]

    async def add_booking(self, _booking_data: BookingAddRequest, hotel_id: int):
        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=_booking_data.date_from,
            date_to=_booking_data.date_to,
            hotel_id=hotel_id,
        )
        result = await self.session.execute(rooms_ids_to_get)
        rooms_ids = result.unique().scalars().all()
        if _booking_data.room_id not in rooms_ids:
            raise AllRoomsAreBookedException

        return await self.add(_booking_data)
