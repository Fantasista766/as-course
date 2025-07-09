from src.models.bookings import BookingsORM
from src.models.facilities import FacilitiesORM, RoomsFacilitiesORM
from src.models.hotels import HotelsORM
from src.models.rooms import RoomsORM
from src.models.users import UsersORM
from src.repositories.mappers.base import DataMapper
from src.schemas.bookings import BookingDTO
from src.schemas.facilities import FacilityDTO, RoomFacilityDTO
from src.schemas.hotels import HotelDTO
from src.schemas.rooms import RoomDTO, RoomWithRelsDTO
from src.schemas.users import UserDTO, UserWithHashedPasswordDTO


class BookingDataMapper(DataMapper):
    model = BookingsORM
    schema = BookingDTO


class FacilityDataMapper(DataMapper):
    model = FacilitiesORM
    schema = FacilityDTO


class HotelDataMapper(DataMapper):
    model = HotelsORM
    schema = HotelDTO


class RoomDataMapper(DataMapper):
    model = RoomsORM
    schema = RoomDTO


class RoomFacilityDataMapper(DataMapper):
    model = RoomsFacilitiesORM
    schema = RoomFacilityDTO


class RoomWithRelsDataMapper(DataMapper):
    model = RoomsORM
    schema = RoomWithRelsDTO


class UserDataMapper(DataMapper):
    model = UsersORM
    schema = UserDTO


class UserWithHashedPasswordDataMapper(DataMapper):
    model = UsersORM
    schema = UserWithHashedPasswordDTO
