from src.models.hotels import HotelsORM
from src.repositories.mappers.base import DataMapper
from src.schemas.hotels import Hotel


class HotelDataMapper(DataMapper):
    model = HotelsORM
    schema = Hotel
