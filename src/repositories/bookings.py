from datetime import date

from sqlalchemy import select

from src.models.bookings import BookingsORM
from src.models.rooms import RoomsORM
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
        return [
            self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()
        ]

    async def add_booking(self, _booking_data: BookingAddRequest):
        # получили id отеля
        query = (
            select(RoomsORM.hotel_id)
            .select_from(RoomsORM)
            .filter_by(id=_booking_data.room_id)
        )
        res = await self.session.execute(query)
        hotel_id = res.scalars().one()

        rooms_ids_to_get = rooms_ids_for_booking(
            _booking_data.date_from, _booking_data.date_to, hotel_id
        )
        query = (
            select(RoomsORM.id)
            .select_from(RoomsORM)
            .filter(RoomsORM.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        rooms_ids = result.unique().scalars().all()
        if _booking_data.room_id not in rooms_ids:
            raise

        return await super().add(_booking_data)
