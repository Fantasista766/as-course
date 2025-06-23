from src.exceptions import (
    FacilityNotFoundException,
    ObjectNotFoundException,
)
from src.schemas.facilities import Facility, FacilityAdd
from src.services.base import BaseService
from src.tasks.tasks import test_task


class FacilityService(BaseService):
    async def get_all_facilities(self) -> list[Facility]:
        return await self.db.facilities.get_all()

    async def create_facility(self, facility_data: FacilityAdd) -> Facility:
        facility = await self.db.facilities.add(facility_data)
        await self.db.commit()

        test_task.delay()  # type: ignore
        return Facility.model_validate(facility)

    async def get_facilities_with_check(self, facilities_ids: list[int]) -> list[Facility]:
        try:
            return await self.db.facilities.get_batch_by_ids(facilities_ids)
        except ObjectNotFoundException:
            raise FacilityNotFoundException
