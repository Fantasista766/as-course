from typing import Generic, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import Row, RowMapping

from src.database import Base

SchemaType = TypeVar("SchemaType", bound=BaseModel)


class DataMapper(Generic[SchemaType]):
    db_model: Type[Base]
    schema: Type[SchemaType]

    @classmethod
    def map_to_domain_entity(cls, data: Base | dict | Row | RowMapping) -> SchemaType:
        return cls.schema.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_persistance_entity(cls, data: BaseModel) -> Base:
        return cls.db_model(**data.model_dump())
