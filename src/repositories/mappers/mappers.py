from src.models.bookings import BookingsORM
from src.models.facilities import FacilitiesORM, RoomsFacilitiesORM
from src.models.hotels import HotelsORM
from src.models.rooms import RoomsORM
from src.models.users import UsersORM
from src.repositories.mappers.base import DataMapper
from src.schemas.bookings import Booking
from src.schemas.facilities import Facility, RoomFacility
from src.schemas.hotels import Hotel
from src.schemas.rooms import Room, RoomWithRels
from src.schemas.users import User, UserWithHashedPassword


class BookingDataMapper(DataMapper):
    model = BookingsORM
    schema = Booking


class FacilityDataMapper(DataMapper):
    model = FacilitiesORM
    schema = Facility


class HotelDataMapper(DataMapper):
    model = HotelsORM
    schema = Hotel


class RoomDataMapper(DataMapper):
    model = RoomsORM
    schema = Room


class RoomFacilityDataMapper(DataMapper):
    model = RoomsFacilitiesORM
    schema = RoomFacility


class RoomWithRelsDataMapper(DataMapper):
    model = RoomsORM
    schema = RoomWithRels


class UserDataMapper(DataMapper):
    model = UsersORM
    schema = User


class UserWithHashedPasswordDataMapper(DataMapper):
    model = UsersORM
    schema = UserWithHashedPassword
