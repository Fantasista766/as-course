from datetime import date
from typing import Any

from sqlalchemy import select

from src.models.hotels import HotelsORM
from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsORM
    schema = Hotel

    async def get_all(
        self,
        location: str | None,
        title: str | None,
        limit: int,
        offset: int,
        *args: Any,
        **kwargs: Any,
    ) -> list[Hotel]:
        query = select(HotelsORM)
        if title:
            query = query.filter(HotelsORM.title.icontains(title.strip()))
        if location:
            query = query.filter(HotelsORM.location.contains(location.strip()))

        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        return [
            Hotel.model_validate(hotel, from_attributes=True)
            for hotel in result.scalars().all()
        ]

    async def get_filtered_by_time(self, date_from: date, date_to: date):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to)
        hotels_ids_to_get = (
            select(RoomsORM.hotel_id)
            .select_from(RoomsORM)
            .filter(RoomsORM.id.in_(rooms_ids_to_get))
        )

        return await self.get_filtered(HotelsORM.id.in_(hotels_ids_to_get))
