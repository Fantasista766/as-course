from typing import Any

from pydantic import BaseModel

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    model: Any = None
    schema: Any = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, *args: tuple[Any], **kwargs: dict[Any, Any]) -> list[Any]:
        query = select(self.model)
        result = await self.session.execute(query)
        return [self.schema.model_validate(model) for model in result.scalars().all()]

    async def get_one_or_none(self, **filter_by: Any) -> Any:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        return self.schema.model_validate(model) if model else model

    async def add(self, data: BaseModel) -> Any:
        add_model_stmt = (
            insert(self.model).values(**data.model_dump()).returning(self.model)
        )
        try:
            result = await self.session.execute(add_model_stmt)
        except Exception as e:
            if "already exists." in e.args[0]:
                return f"Пользователь с такими данными уже зарегистрирован"
            return f"Не удалось создать пользователя"
        model = result.scalars().one()
        return self.schema.model_validate(model) if model else model

    async def edit(
        self, data: BaseModel, exclude_unset: bool = False, **filter_by: Any
    ) -> int | None:
        result = await self.get_one_or_none(**filter_by)
        if not result:
            return 404
        edit_model_stmt = (
            update(self.model)
            .values(**data.model_dump(exclude_unset=exclude_unset))
            .filter_by(**filter_by)
        )
        await self.session.execute(edit_model_stmt)

    async def delete(self, **filter_by: Any) -> int | None:
        result = await self.get_one_or_none(**filter_by)
        if not result:
            return 404
        delete_model_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_model_stmt)
