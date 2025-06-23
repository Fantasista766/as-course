from typing import Any

from asyncpg.exceptions import ForeignKeyViolationError, UniqueViolationError
from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import (
    ObjectAlreadyExistsException,
    ObjectNotFoundException,
    ObjectToDeleteHasActiveRelations,
)


class BaseRepository:
    model: Any = None
    mapper: Any = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_filtered(self, *filter: Any, **filter_by: Any) -> list[Any]:
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_all(self, *args: Any, **kwargs: Any) -> list[Any]:
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by: Any) -> Any:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        return self.mapper.map_to_domain_entity(model) if model else model

    async def get_one(self, **filter_by: Any) -> Any:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            model = result.scalar_one()
        except NoResultFound:
            raise ObjectNotFoundException
        return self.mapper.map_to_domain_entity(model)

    async def add(self, data: BaseModel) -> Any:
        add_model_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result: Any = None
        try:
            result = await self.session.execute(add_model_stmt)
        except IntegrityError as ex:
            if isinstance(ex.orig.__cause__, ForeignKeyViolationError):  # type: ignore
                raise ObjectNotFoundException
            if isinstance(ex.orig.__cause__, UniqueViolationError):  # type: ignore
                raise ObjectAlreadyExistsException
            raise ex
        model = result.scalars().one()
        return self.mapper.map_to_domain_entity(model)

    async def add_batch(self, data: list[Any]) -> Any:
        add_model_stmt = (
            insert(self.model).values([item.model_dump() for item in data]).returning(self.model)
        )
        try:
            await self.session.execute(add_model_stmt)
        except Exception:
            raise ObjectNotFoundException

    async def edit(
        self, data: BaseModel, exclude_unset: bool = False, **filter_by: Any
    ) -> int | None:
        await self.get_one(**filter_by)
        edit_model_stmt = (
            update(self.model)
            .values(**data.model_dump(exclude_unset=exclude_unset))
            .filter_by(**filter_by)
        )
        await self.session.execute(edit_model_stmt)

    async def delete(self, **filter_by: Any) -> int | None:
        await self.get_one(**filter_by)
        delete_model_stmt = delete(self.model).filter_by(**filter_by)
        try:
            await self.session.execute(delete_model_stmt)
        except IntegrityError:
            raise ObjectToDeleteHasActiveRelations

    async def delete_batch_by_ids(self, ids_to_delete: list[int]) -> int | None:
        delete_model_stmt = delete(self.model).where(self.model.id.in_(ids_to_delete))
        await self.session.execute(delete_model_stmt)
