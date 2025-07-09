from pydantic import BaseModel, Field, model_validator

from src.exceptions import HotelPatchEmptyBodyException


class HotelAddDTO(BaseModel):
    title: str = Field(..., min_length=5)
    location: str = Field(..., min_length=10)


class HotelDTO(HotelAddDTO):
    id: int


class HotelPatchDTO(BaseModel):
    title: str | None = Field(None, min_length=5)
    location: str | None = Field(None, min_length=10)

    @model_validator(mode="after")
    def at_least_one_field(cls, model):
        if not model.title and not model.location:
            raise HotelPatchEmptyBodyException
        return model
