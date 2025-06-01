from typing import List

from fastapi import APIRouter, Body, Query
from sqlalchemy import func, insert, select

from src.models.hotels import HotelsORM
from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get(
    "/",
    summary="Получить список отелей",
)
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Расположение отеля"),
) -> List[Hotel]:
    per_page = pagination.per_page or 5
    page = pagination.page or 1
    async with async_session_maker() as session:
        query = select(HotelsORM)
        if title:
            query.filter(func.lower(HotelsORM.title).contains(title.title().lower()))
        if location:
            query.filter(
                func.lower(HotelsORM.location).contains(location.strip().lower())
            )

        query = query.limit(per_page).offset((page - 1) * per_page)
        result = await session.execute(query)
        hotels = result.scalars().all()
        return hotels


@router.post("/", summary="Создать новый отель")
async def create_hotel(
    hotel_data: Hotel = Body(
        openapi_examples={
            "1": {
                "summary": "Sochi",
                "value": {
                    "title": "Hotel Sochi 5 start near sea",
                    "location": "ул. Моря, 1",
                },
            },
            "2": {
                "summary": "Dubai",
                "value": {
                    "title": "Hotel Dubai 5 star with pool",
                    "location": "ул. Шейха, 2",
                },
            },
        }
    )
):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsORM).values(**hotel_data.model_dump())
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"status": "OK"}


@router.put("/{hotel_id}", summary="Обновить данные об отеле")
def update_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["location"] = hotel_data.location
            return {"status": "OK"}
    return {"status": "Hotel not found"}, 404


@router.patch(
    "/{hotel_id}",
    summary="Частично обновить данные об отеле",
    description="Позволяет обновить только некоторые поля отеля, такие как название или имя.",
)
def partial_update_hotel(
    hotel_id: int,
    hotel_data: HotelPATCH,
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title is not None:
                hotel["title"] = hotel_data.title
            if hotel_data.location is not None:
                hotel["location"] = hotel_data.location
            return {"status": "OK"}
    return {"status": "Hotel not found"}, 404


@router.delete("/{hotel_id}", summary="Удалить отель")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}
