from typing import Any

from fastapi import APIRouter, Body, Query

from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import Hotel, HotelPATCH, HotelAdd

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get(
    "/",
    summary="Получить список отелей",
)
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Расположение отеля"),
) -> list[Hotel]:
    per_page = pagination.per_page or 5
    page = pagination.page or 1
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=(page - 1) * per_page,
        )


@router.get("/{hotel_id}", summary="Получить отель")
async def get_hotel(hotel_id: int) -> Hotel:
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id=hotel_id)


@router.post("/", summary="Создать новый отель")
async def create_hotel(
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
    )
) -> Any:
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"status": "OK", "data": Hotel.model_validate(hotel)}


@router.put("/{hotel_id}", summary="Обновить данные об отеле")
async def update_hotel(hotel_id: int, hotel_data: HotelAdd):
    async with async_session_maker() as session:
        result = await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
    if result == 404:
        return {"status": "Hotel not found"}, 404
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Частично обновить данные об отеле",
    description="Позволяет обновить только некоторые поля отеля, такие как название или имя.",
)
async def partial_update_hotel(
    hotel_id: int,
    hotel_data: HotelPATCH,
):
    async with async_session_maker() as session:
        result = await HotelsRepository(session).edit(
            hotel_data, exclude_unset=True, id=hotel_id
        )
        await session.commit()
    if result == 404:
        return {"status": "Hotel not found"}, 404
    return {"status": "OK"}


@router.delete("/{hotel_id}", summary="Удалить отель")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        result = await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    if result == 404:
        return {"status": "Hotel not found"}, 404
    return {"status": "OK"}
