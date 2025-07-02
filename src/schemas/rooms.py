from pydantic import BaseModel, ConfigDict, Field, model_validator

from src.exceptions import RoomPatchEmptyBodyException
from src.schemas.facilities import Facility


class RoomAddRequest(BaseModel):
    title: str = Field(..., min_length=2)
    description: str | None = None
    price: int = Field(..., ge=1)
    quantity: int = Field(..., ge=1)
    facilities_ids: list[int] | None = None


class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    description: str | None = None
    price: int
    quantity: int


class Room(RoomAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomWithRels(Room):
    facilities: list[Facility]


class RoomPatchRequest(BaseModel):
    title: str | None = Field(None, min_length=2)
    description: str | None = None
    price: int | None = Field(None, ge=1)
    quantity: int | None = Field(None, ge=1)
    facilities_ids: list[int] | None = None

    @model_validator(mode="after")
    def at_least_one_field(cls, model):
        if all(getattr(model, field, None) is None for field in model.model_fields):
            raise RoomPatchEmptyBodyException
        return model


class RoomPatch(BaseModel):
    hotel_id: int | None = None
    title: str | None = Field(None, min_length=2)
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
