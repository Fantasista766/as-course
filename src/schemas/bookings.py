from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class BookingAddDTO(BaseModel):
    room_id: int = Field(..., ge=1)
    date_from: date
    date_to: date


class BookingAddRequestDTO(BookingAddDTO):
    user_id: int
    price: int
    create_at: datetime | None = None


class BookingDTO(BookingAddRequestDTO):
    id: int

    model_config = ConfigDict(from_attributes=True)
