from typing import List, Dict, Any

from fastapi import APIRouter, Body, Query

router = APIRouter(prefix="/hotels", tags=["Отели"])


hotels: List[Dict[str, Any]] = [
    {"id": 1, "title": "Sochi", "name": "Sochi"},
    {"id": 2, "title": "Dubai", "name": "Dubai"},
]


@router.get("/", summary="Получить список отелей")
def get_hotels(
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
    return hotels_


@router.post("/", summary="Создать новый отель")
def create_hotel(title: str = Body(embed=True)):
    global hotels
    hotels.append(
        {
            "id": hotels[-1]["id"] + 1,
            "title": title,
        }
    )
    return {"status": "OK"}


@router.put("/{hotel_id}", summary="Обновить данные об отеле")
def update_hotel(
    hotel_id: int,
    title: str = Body(description="Новое название отеля"),
    name: str = Body(description="Новое имя отеля"),
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name
            return {"status": "OK"}
    return {"status": "Hotel not found"}, 404


@router.patch(
    "/{hotel_id}",
    summary="Частично обновить данные об отеле",
    description="Позволяет обновить только некоторые поля отеля, такие как название или имя.",
)
def partial_update_hotel(
    hotel_id: int,
    title: str | None = Body(None, description="Новое название отеля"),
    name: str | None = Body(None, description="Новое имя отеля"),
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if title is not None:
                hotel["title"] = title
            if name is not None:
                hotel["name"] = name
            return {"status": "OK"}
    return {"status": "Hotel not found"}, 404


@router.delete("/{hotel_id}", summary="Удалить отель")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}
