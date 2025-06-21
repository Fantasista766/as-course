from datetime import date

from fastapi import APIRouter, HTTPException, Body, Query
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep, PaginationDep
from src.schemas.hotels import Hotel, HotelPatch, HotelAdd

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get(
    "/",
    summary="Получить список отелей",
)
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Расположение отеля"),
    date_from: date = Query(examples=["2025-06-19"]),
    date_to: date = Query(examples=["2025-06-29"]),
) -> list[Hotel]:
    per_page = pagination.per_page or 5
    page = pagination.page or 1
    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        location=location,
        title=title,
        limit=per_page,
        offset=(page - 1) * per_page,
    )


@router.get("/{hotel_id}", summary="Получить отель")
@cache(expire=10)
async def get_hotel(db: DBDep, hotel_id: int) -> Hotel | None:
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.post("/", summary="Создать новый отель")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Sochi",
                "value": {
                    "title": "Hotel 5 start near sea",
                    "location": "Сочи, ул. Моря, 1",
                },
            },
            "2": {
                "summary": "Dubai",
                "value": {
                    "title": "Hotel 5 star with pool",
                    "location": "Дубай, ул. Шейха, 2",
                },
            },
        }
    ),
) -> dict[str, str | Hotel]:
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status": "OK", "data": Hotel.model_validate(hotel)}


@router.put("/{hotel_id}", summary="Обновить данные об отеле")
async def update_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAdd):
    result = await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    if result == 404:
        raise HTTPException(status_code=404, detail="Отель не найден")
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Частично обновить данные об отеле",
    description="Позволяет обновить только некоторые поля отеля, такие как название или имя.",
)
async def partial_update_hotel(
    db: DBDep,
    hotel_id: int,
    hotel_data: HotelPatch,
):
    result = await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    if result == 404:
        raise HTTPException(status_code=404, detail="Отель не найден")
    return {"status": "OK"}


@router.delete("/{hotel_id}", summary="Удалить отель")
async def delete_hotel(db: DBDep, hotel_id: int):
    result = await db.hotels.delete(id=hotel_id)
    await db.commit()
    if result == 404:
        raise HTTPException(status_code=404, detail="Отель не найден")
    return {"status": "OK"}
