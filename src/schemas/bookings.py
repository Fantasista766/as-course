from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class BookingAdd(BaseModel):
    room_id: int = Field(..., ge=1)
    date_from: date
    date_to: date


class BookingAddRequest(BookingAdd):
    user_id: int
    price: int
    create_at: datetime | None = None


class Booking(BookingAddRequest):
    id: int

    model_config = ConfigDict(from_attributes=True)
