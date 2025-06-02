from typing import Sequence

from sqlalchemy import select

from src.repositories.base import BaseRepository
from src.models.hotels import HotelsORM


class HotelsRepository(BaseRepository):
    model = HotelsORM

    async def get_all(
        self, location: str, title: str, limit: int, offset: int, *args, **kwargs
    ) -> Sequence[HotelsORM]:
        query = select(HotelsORM)
        if title:
            query = query.filter(HotelsORM.title.icontains(title.strip()))
        if location:
            query = query.filter(HotelsORM.location.contains(location.strip()))

        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        return result.scalars().all()
