from datetime import date

from sqlalchemy import select

from src.models.hotels import HotelsORM
from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import HotelDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsORM
    mapper = HotelDataMapper

    async def get_filtered_by_time(
        self,
        date_from: date,
        date_to: date,
        location: str | None,
        title: str | None,
        limit: int,
        offset: int,
    ) -> list[Hotel]:
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to)
        hotels_ids_to_get = (
            select(RoomsORM.hotel_id)
            .select_from(RoomsORM)
            .filter(RoomsORM.id.in_(rooms_ids_to_get))
        )
        query = select(HotelsORM).filter(HotelsORM.id.in_(hotels_ids_to_get))

        if title:
            query = query.filter(HotelsORM.title.icontains(title.strip()))
        if location:
            query = query.filter(HotelsORM.location.contains(location.strip()))

        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)

        return [
            self.mapper.map_to_domain_entity(hotel) for hotel in result.scalars().all()
        ]
