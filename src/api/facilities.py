from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import Facility, FacilityAdd

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("/", summary="Получить список удобств")
@cache(10)
async def get_facilities(db: DBDep) -> list[Facility]:
    return await db.facilities.get_all()


@router.post("/", summary="Создать новое удобство")
async def create_facility(
    db: DBDep,
    facility_data: FacilityAdd = Body(
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
) -> dict[str, str | Facility]:
    facility = await db.facilities.add(facility_data)
    await db.commit()
    return {"status": "OK", "data": Facility.model_validate(facility)}
