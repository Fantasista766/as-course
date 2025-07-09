from datetime import date

from src.exceptions import (
    FacilityNotFoundException,
    ObjectAlreadyExistsException,
    ObjectToDeleteHasActiveRelationsException,
    ObjectNotFoundException,
    HotelNotFoundException,
    RoomAlreadyExistsException,
    RoomNotFoundException,
    RoomToDeleteHasActiveBookingsException,
    check_date_from_before_date_to,
)
from src.schemas.facilities import RoomFacilityAddDTO
from src.schemas.rooms import (
    RoomDTO,
    RoomAddDTO,
    RoomAddRequestDTO,
    RoomPatchDTO,
    RoomPatchRequestDTO,
    RoomWithRelsDTO,
)
from src.services.base import BaseService
from src.services.facilities import FacilityService
from src.services.hotels import HotelService


class RoomService(BaseService):
    async def get_filtered_by_time(
        self, hotel_id: int, date_from: date, date_to: date
    ) -> list[RoomWithRelsDTO]:
        check_date_from_before_date_to(date_from, date_to)
        return await self.db.rooms.get_filtered_by_time(  # type: ignore
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )

    async def get_one_with_rels(self, room_id: int, hotel_id: int) -> RoomWithRelsDTO:
        return await self.db.rooms.get_one_with_rels(id=room_id, hotel_id=hotel_id)  # type: ignore

    async def add_room(self, hotel_id: int, room_data: RoomAddRequestDTO) -> RoomDTO:
        try:
            await self.db.hotels.get_one(id=hotel_id)  # type: ignore
        except ObjectNotFoundException:
            raise HotelNotFoundException

        _room_data = RoomAddDTO(hotel_id=hotel_id, **room_data.model_dump())
        try:
            room = await self.db.rooms.add(_room_data)  # type: ignore
        except ObjectAlreadyExistsException:
            raise RoomAlreadyExistsException

        if room_data.facilities_ids:
            rooms_facilities_data = [
                RoomFacilityAddDTO(room_id=room.id, facility_id=f_id)
                for f_id in room_data.facilities_ids
            ]
            try:
                await self.db.rooms_facilities.add_batch(rooms_facilities_data)  # type: ignore
            except ObjectNotFoundException:
                raise FacilityNotFoundException
        await self.db.commit()  # type: ignore

        return RoomDTO.model_validate(room)

    async def edit_room(self, hotel_id: int, room_id: int, room_data: RoomAddRequestDTO) -> None:
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        await self.get_room_with_check(room_id)

        _room_data = RoomAddDTO(hotel_id=hotel_id, **room_data.model_dump())
        await self.db.rooms.edit(_room_data, id=room_id, hotel_id=hotel_id)  # type: ignore
        if room_data.facilities_ids is not None:
            await FacilityService(self.db).get_facilities_with_check(room_data.facilities_ids)
            try:
                await self.db.rooms_facilities.set_room_facilities(  # type: ignore
                    room_id, facilities_ids=room_data.facilities_ids
                )
            except ObjectNotFoundException:
                raise FacilityNotFoundException

        await self.db.commit()  # type: ignore

    async def partial_edit_room(
        self,
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequestDTO,
    ) -> None:
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        await self.get_room_with_check(room_id)

        _room_data_dict = room_data.model_dump(exclude_unset=True)
        _room_data = RoomPatchDTO(hotel_id=hotel_id, **_room_data_dict)
        await self.db.rooms.edit(_room_data, id=room_id, hotel_id=hotel_id)  # type: ignore
        if room_data.facilities_ids:
            await FacilityService(self.db).get_facilities_with_check(room_data.facilities_ids)
            await self.db.rooms_facilities.set_room_facilities(  # type: ignore
                room_id, facilities_ids=room_data.facilities_ids
            )
        await self.db.commit()  # type: ignore

    async def delete_room(self, hotel_id: int, room_id: int) -> None:
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        await self.get_room_with_check(room_id)
        try:
            await self.db.rooms.delete(id=room_id, hotel_id=hotel_id)  # type: ignore
        except ObjectToDeleteHasActiveRelationsException:
            raise RoomToDeleteHasActiveBookingsException

        await self.db.commit()  # type: ignore

    async def get_room_with_check(self, room_id: int) -> RoomDTO:
        try:
            return await self.db.rooms.get_one(id=room_id)  # type: ignore
        except ObjectNotFoundException:
            raise RoomNotFoundException
