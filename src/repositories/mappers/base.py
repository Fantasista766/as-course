from typing import Any


class DataMapper:
    db_model: Any = None
    schema: Any = None

    @classmethod
    def map_to_domain_entity(cls, data: Any) -> Any:
        return cls.schema.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_persistance_entity(cls, data: Any) -> Any:
        return cls.db_model(**data.model_dump())
