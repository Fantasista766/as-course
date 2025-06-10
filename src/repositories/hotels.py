from typing import Any

from sqlalchemy import select

from src.models.hotels import HotelsORM
from src.repositories.base import BaseRepository
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
