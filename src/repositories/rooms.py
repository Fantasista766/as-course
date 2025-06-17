from datetime import date
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_booking
from src.models.rooms import RoomsORM
from src.schemas.rooms import Room, RoomWithRels


class RoomsRepository(BaseRepository):
    model = RoomsORM
    schema = Room

    async def get_filtered_by_time(
        self, hotel_id: int, date_from: date, date_to: date
    ) -> list[RoomWithRels]:
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomsORM.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        return [
            RoomWithRels.model_validate(model)
            for model in result.unique().scalars().all()
        ]

    async def get_one_or_none(self, **filter_by: Any) -> RoomWithRels | None:
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        return RoomWithRels.model_validate(model) if model else model
