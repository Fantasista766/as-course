from src.exceptions import (
    FacilityAlreadyExistsException,
    FacilityNotFoundException,
    ObjectAlreadyExistsException,
    ObjectNotFoundException,
)
from src.schemas.facilities import FacilityDTO, FacilityAddDTO
from src.services.base import BaseService
from src.tasks.tasks import test_task


class FacilityService(BaseService):
    async def get_all_facilities(self) -> list[FacilityDTO]:
        return await self.db.facilities.get_all()  # type: ignore

    async def create_facility(self, facility_data: FacilityAddDTO) -> FacilityDTO:
        try:
            facility = await self.db.facilities.add(facility_data)  # type: ignore
        except ObjectAlreadyExistsException:
            raise FacilityAlreadyExistsException
        await self.db.commit()  # type: ignore

        test_task.delay()  # type: ignore
        return FacilityDTO.model_validate(facility)

    async def get_facilities_with_check(self, facilities_ids: list[int]) -> list[FacilityDTO]:
        try:
            return await self.db.facilities.get_batch_by_ids(facilities_ids)  # type: ignore
        except ObjectNotFoundException:
            raise FacilityNotFoundException
