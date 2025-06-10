from datetime import date

from pydantic import BaseModel


class BookingAdd(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class BookingAddRequest(BookingAdd):
    user_id: int
    price: int


class Booking(BookingAddRequest):
    id: int

    class Config:
        from_attributes = True
