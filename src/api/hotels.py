from datetime import date

from fastapi import APIRouter, Body, Query
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep, PaginationDep
from src.exceptions import (
    HotelNotFoundHTTPException,
    ObjectNotFoundException,
)
from src.schemas.hotels import Hotel, HotelPatch, HotelAdd
from src.services.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get(
    "/",
    summary="Получить список отелей с доступными номерами",
)
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Расположение отеля"),
    date_from: date = Query(example="2025-06-19"),
    date_to: date = Query(example="2025-06-29"),
) -> list[Hotel]:
    return await HotelService(db).get_filtered_by_time(
        pagination, title, location, date_from, date_to
    )


@router.get("/{hotel_id}", summary="Получить отель")
@cache(expire=10)
async def get_hotel(db: DBDep, hotel_id: int) -> Hotel:
    try:
        return await HotelService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


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
    hotel = await HotelService(db).add_hotel(hotel_data)
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}", summary="Обновить данные об отеле")
async def update_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAdd) -> dict[str, str]:
    try:
        await HotelService(db).edit_hotel(hotel_id, hotel_data)
        return {"status": "OK"}
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.patch(
    "/{hotel_id}",
    summary="Частично обновить данные об отеле",
    description="Позволяет обновить только некоторые поля отеля, такие как название или имя.",
)
async def partial_update_hotel(
    db: DBDep,
    hotel_id: int,
    hotel_data: HotelPatch,
) -> dict[str, str]:
    try:
        await HotelService(db).edit_hotel(hotel_id, hotel_data, exclude_unset=True)
        return {"status": "OK"}
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.delete("/{hotel_id}", summary="Удалить отель")
async def delete_hotel(db: DBDep, hotel_id: int) -> dict[str, str]:
    try:
        await HotelService(db).delete_hotel(hotel_id)
        return {"status": "OK"}
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
