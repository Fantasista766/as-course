from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class BookingAdd(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class BookingAddRequest(BookingAdd):
    user_id: int
    price: int
    create_at: datetime


class Booking(BookingAddRequest):
    id: int

    model_config = ConfigDict(from_attributes=True)
