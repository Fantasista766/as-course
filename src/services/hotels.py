from datetime import date

from src.api.dependencies import PaginationDep
from src.exceptions import check_date_from_before_date_to
from src.schemas.hotels import Hotel, HotelAdd, HotelPatch
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
        return await self.db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            limit=per_page,
            offset=(page - 1) * per_page,
        )

    async def get_hotel(self, hotel_id: int) -> Hotel:
        return await self.db.hotels.get_one(id=hotel_id)

    async def add_hotel(self, hotel_data: HotelAdd) -> dict[str, str | Hotel]:
        hotel = await self.db.hotels.add(hotel_data)
        await self.db.commit()
        return {"status": "OK", "data": Hotel.model_validate(hotel)}

    async def edit_hotel(
        self, hotel_id: int, hotel_data: HotelAdd | HotelPatch, exclude_unset: bool = False
    ) -> dict[str, str]:
        await self.db.hotels.edit(hotel_data, id=hotel_id, exclude_unset=exclude_unset)
        await self.db.commit()
        return {"status": "OK"}

    async def delete_hotel(self, hotel_id: int) -> dict[str, str]:
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()
        return {"status": "OK"}
