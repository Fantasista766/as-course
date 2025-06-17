from sqlalchemy import select

from src.models.facilities import FacilitiesORM, RoomsFacilitiesORM

from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import FacilityDataMapper, RoomFacilityDataMapper
from src.schemas.facilities import RoomFacilityAdd


class FacilitiesRepository(BaseRepository):
    model = FacilitiesORM
    mapper = FacilityDataMapper


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesORM
    mapper = RoomFacilityDataMapper

    async def set_room_facilities(
        self, room_id: int, facilities_ids: list[int]
    ) -> None:
        # достаём все удобства номера
        get_current_facilities_query = select(self.model.facility_id).filter_by(
            room_id=room_id
        )
        res = await self.session.execute(get_current_facilities_query)
        current_room_facilities_ids = res.scalars().all()
        ids_to_delete = list(set(current_room_facilities_ids) - set(facilities_ids))
        ids_to_insert = list(set(facilities_ids) - set(current_room_facilities_ids))

        room_facilities_to_add = [
            RoomFacilityAdd(room_id=room_id, facility_id=f_id) for f_id in ids_to_insert
        ]

        await self.add_batch(room_facilities_to_add)  # type: ignore
        await self.delete_batch_by_ids(ids_to_delete)  # type: ignore
