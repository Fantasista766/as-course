from typing import Any, TypeVar

from pydantic import BaseModel

from src.database import Base

DBModelType = TypeVar("DBModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class DataMapper:
    db_model: type[DBModelType] = None  # type: ignore
    schema: type[SchemaType] = None  # type: ignore

    @classmethod
    def map_to_domain_entity(cls, data: Any) -> Any:
        return cls.schema.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_persistance_entity(cls, data: Any) -> Any:
        return cls.db_model(**data.model_dump())
