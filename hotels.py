from typing import List, Dict, Any

from fastapi import APIRouter, Body, Query

from dependencies import PaginationDep
from schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])


hotels: List[Dict[str, Any]] = [
    {"id": 1, "title": "Сочи", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@router.get("/", summary="Получить список отелей")
def get_hotels(
    pagination: PaginationDep,
    id: int | None = Query(None, description="ID отеля"),
    title: str | None = Query(None, description="Название отеля"),
) -> List[Dict[str, Any]]:
    hotels_: List[Dict[str, Any]] = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)

    if pagination.page is not None and pagination.per_page is not None:
        return hotels_[(pagination.page - 1) * pagination.per_page :][
            : pagination.per_page
        ]
    return hotels_


@router.post("/", summary="Создать новый отель")
def create_hotel(
    hotel_data: Hotel = Body(
        openapi_examples={
            "1": {
                "summary": "Sochi",
                "value": {
                    "title": "Holel Sochi 5 start near sea",
                    "name": "Sochi near sea",
                },
            },
            "2": {
                "summary": "Dubai",
                "value": {
                    "title": "Hotel Dubai 5 star with pool",
                    "name": "Dubai luxury hotel",
                },
            },
        }
    )
):
    global hotels
    hotels.append(
        {
            "id": hotels[-1]["id"] + 1,
            "title": hotel_data.title,
            "name": hotel_data.name,
        }
    )
    return {"status": "OK"}


@router.put("/{hotel_id}", summary="Обновить данные об отеле")
def update_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name
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
            if hotel_data.name is not None:
                hotel["name"] = hotel_data.name
            return {"status": "OK"}
    return {"status": "Hotel not found"}, 404


@router.delete("/{hotel_id}", summary="Удалить отель")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}
