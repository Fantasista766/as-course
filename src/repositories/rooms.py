from datetime import date

from sqlalchemy import func, select

from src.repositories.base import BaseRepository
from src.models.bookings import BookingsORM
from src.models.rooms import RoomsORM
from src.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsORM
    schema = Room

    async def get_filtered_by_time(self, hotel_id: int, date_from: date, date_to: date):
        rooms_count = (
            select(BookingsORM.room_id, func.count("*").label("rooms_booked"))
            .select_from(BookingsORM)
            .filter(
                BookingsORM.date_from <= date_to,
                BookingsORM.date_to >= date_from,
            )
            .group_by(BookingsORM.room_id)
            .cte(name="rooms_count")
        )
        rooms_left_table = (
            select(
                RoomsORM.id.label("room_id"),
                (
                    RoomsORM.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)
                ).label("rooms_left"),
            )
            .select_from(RoomsORM)
            .outerjoin(rooms_count, RoomsORM.id == rooms_count.c.room_id)
            .cte(name="rooms_left_table")
        )
        rooms_ids_for_hotel = (
            select(RoomsORM.id)
            .select_from(RoomsORM)
            .filter(RoomsORM.hotel_id == hotel_id)
            .subquery()
        )
        rooms_ids_to_get = (
            select(rooms_left_table.c.room_id)
            .select_from(rooms_left_table)
            .filter(
                rooms_left_table.c.rooms_left > 0,
                rooms_left_table.c.room_id.in_(rooms_ids_for_hotel),  # type: ignore
            )
        )

        return await self.get_filtered(RoomsORM.id.in_(rooms_ids_to_get))
