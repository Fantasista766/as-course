from datetime import date
from typing import Any

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload

from src.exceptions import RoomNotFoundException
from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import RoomDataMapper, RoomWithRelsDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.rooms import RoomWithRels


class RoomsRepository(BaseRepository):
    model = RoomsORM
    mapper = RoomDataMapper

    async def get_filtered_by_time(
        self, hotel_id: int, date_from: date, date_to: date
    ) -> list[RoomWithRels]:
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(self.model.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        return [
            RoomWithRelsDataMapper.map_to_domain_entity(model)
            for model in result.unique().scalars().all()
        ]

    async def get_one_with_rels(self, **filter_by: Any) -> RoomWithRels:
        query = (
            select(self.model).options(selectinload(self.model.facilities)).filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        try:
            model = result.scalars().one()
        except NoResultFound:
            raise RoomNotFoundException
        return RoomWithRelsDataMapper.map_to_domain_entity(model) if model else model
