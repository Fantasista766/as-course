from typing import Any, Sequence

from pydantic import BaseModel

from sqlalchemy import delete, insert, select, update
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

    async def get_one_or_none(self, **filter_by: dict[str, Any]) -> Any:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)

        return result.scalars().one_or_none()

    async def add(self, data: BaseModel) -> Any:
        add_model_stmt = (
            insert(self.model).values(**data.model_dump()).returning(self.model)
        )
        result = await self.session.execute(add_model_stmt)
        return result.scalars().one()

    async def edit(self, data: BaseModel, **filter_by: dict[str, Any]) -> int | None:
        result = await self.get_one_or_none(**filter_by)
        if not result:
            return 404
        edit_model_stmt = (
            update(self.model).values(**data.model_dump()).filter_by(**filter_by)
        )
        await self.session.execute(edit_model_stmt)

    async def delete(self, **filter_by: dict[str, Any]) -> int | None:
        result = await self.get_one_or_none(**filter_by)
        if not result:
            return 404
        delete_model_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_model_stmt)
