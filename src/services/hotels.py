from datetime import date

from src.api.dependencies import PaginationDep
from src.exceptions import (
    HotelAlreadyExistsException,
    HotelNotFoundException,
    ObjectAlreadyExistsException,
    ObjectNotFoundException,
    check_date_from_before_date_to,
)
from src.schemas.hotels import HotelDTO, HotelAddDTO, HotelPatchDTO
from src.services.base import BaseService


class HotelService(BaseService):
    async def get_filtered_by_time(
        self,
        pagination: PaginationDep,
        title: str | None,
        location: str | None,
        date_from: date,
        date_to: date,
    ):
        check_date_from_before_date_to(date_from, date_to)
        per_page = pagination.per_page or 5
        page = pagination.page or 1
        return await self.db.hotels.get_filtered_by_time(  # type: ignore
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            limit=per_page,
            offset=(page - 1) * per_page,
        )

    async def get_hotel(self, hotel_id: int) -> HotelDTO:
        return await self.db.hotels.get_one(id=hotel_id)  # type: ignore

    async def add_hotel(self, hotel_data: HotelAddDTO) -> HotelDTO:
        try:
            hotel = await self.db.hotels.add(hotel_data)  # type: ignore
        except ObjectAlreadyExistsException:
            raise HotelAlreadyExistsException
        await self.db.commit()  # type: ignore
        return HotelDTO.model_validate(hotel)

    async def edit_hotel(self, hotel_id: int, hotel_data: HotelAddDTO) -> None:
        await self.db.hotels.edit(hotel_data, id=hotel_id)  # type: ignore
        await self.db.commit()  # type: ignore

    async def partial_edit_hotel(self, hotel_id: int, hotel_data: HotelPatchDTO) -> None:
        await self.db.hotels.edit(hotel_data, id=hotel_id, exclude_unset=True)  # type: ignore
        await self.db.commit()  # type: ignore

    async def delete_hotel(self, hotel_id: int) -> None:
        await self.db.hotels.delete(id=hotel_id)  # type: ignore
        await self.db.commit()  # type: ignore

    async def get_hotel_with_check(self, hotel_id: int) -> HotelDTO:
        try:
            return await self.db.hotels.get_one(id=hotel_id)  # type: ignore
        except ObjectNotFoundException:
            raise HotelNotFoundException
