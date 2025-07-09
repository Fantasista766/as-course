from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.exceptions import FacilityAlreadyExistsException, FacilityAlreadyExistsHTTPException
from src.schemas.facilities import FacilityDTO, FacilityAddDTO
from src.services.facilities import FacilityService

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("/", summary="Получить список удобств")
@cache(10)
async def get_facilities(db: DBDep) -> list[FacilityDTO]:
    return await FacilityService(db).get_all_facilities()


@router.post("/", summary="Создать новое удобство")
async def create_facility(
    db: DBDep,
    facility_data: FacilityAddDTO = Body(
        openapi_examples={
            "1": {
                "summary": "Internet",
                "value": {
                    "title": "Интернет",
                },
            },
            "2": {
                "summary": "Air conditioning",
                "value": {
                    "title": "Кондиционер",
                },
            },
        }
    ),
) -> dict[str, str | FacilityDTO]:
    try:
        facility = await FacilityService(db).create_facility(facility_data)
    except FacilityAlreadyExistsException:
        raise FacilityAlreadyExistsHTTPException
    return {"status": "OK", "data": facility}
