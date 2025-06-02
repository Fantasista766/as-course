from typing import Any, Sequence

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    model: Any = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(
        self, *args: tuple[Any], **kwargs: dict[Any, Any]
    ) -> Sequence[Any]:
        query = select(self.model)
        result = await self.session.execute(query)

        return result.scalars().all()

    async def get_one_or_none(self, **filter_by: dict[str, Any]):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)

        return result.scalars().one_or_none()

    async def add(self, *args, **kwargs):
        add_model_stmt = insert(self.model).values(kwargs)
        return await self.session.execute(add_model_stmt)
