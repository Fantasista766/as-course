import json

from fastapi import APIRouter, Body

from src.api.dependencies import DBDep
from src.init import redis_manager
from src.schemas.facilities import Facility, FacilityAdd

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("/", summary="Получить список удобств")
async def get_facilities(db: DBDep) -> list[Facility]:
    facilities_from_cache = await redis_manager.get("facilities")
    if not facilities_from_cache:
        print("BASE")
        facilities = await db.facilities.get_all()
        facilities_schemas = [f.model_dump() for f in facilities]
        facilities_json = json.dumps(facilities_schemas)
        await redis_manager.set("facilities", facilities_json, 10)
        return facilities

    facilites_dicts = json.loads(facilities_from_cache)
    return facilites_dicts


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
