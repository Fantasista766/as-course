from datetime import date
from typing import Any

from fastapi import APIRouter, HTTPException, Body, Query

from src.api.dependencies import DBDep, HotelIdDep, check_hotel_existence
from src.schemas.rooms import Room, RoomPatch, RoomAdd

router = APIRouter(prefix="/hotels/{hotel_id}/rooms", tags=["Номера в отеле"])


@router.get(
    "/",
    summary="Получить список номеров отеля",
)
async def get_rooms(
    db: DBDep,
    hotel_id: HotelIdDep,
    date_from: date = Query(example="2025-06-10"),
    date_to: date = Query(example="2025-06-20"),
) -> list[Room]:
    return await db.rooms.get_filtered_by_time(
        hotel_id=hotel_id, date_from=date_from, date_to=date_to
    )


@router.get("/{room_id}", summary="Получить номер в отеле")
async def get_room(db: DBDep, hotel_id: HotelIdDep, room_id: int) -> Room | None:
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/", summary="Создать новый номер в отеле")
async def create_room(
    db: DBDep,
    room_data: RoomAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Luxury",
                "value": {
                    "hotel_id": 1,
                    "title": "Анаконда",
                    "description": "Всё включено",
                    "price": 1000,
                    "quantity": 10,
                },
            },
            "2": {
                "summary": "Basic",
                "value": {
                    "hotel_id": 1,
                    "title": "Кобра",
                    "description": "Основные удобства",
                    "price": 300,
                    "quantity": 50,
                },
            },
        }
    ),
) -> dict[str, str | Room]:
    # не хочу отдельно hotel_id принимать как параметр функции, поэтому напрямую вызвал функцию из dependencies
    await check_hotel_existence(db=db, hotel_id=room_data.hotel_id)

    room = await db.rooms.add(room_data)
    await db.commit()

    return {"status": "OK", "data": Room.model_validate(room)}


@router.put("/{room_id}", summary="Обновить данные о номере в отеле")
async def update_room(
    db: DBDep, hotel_id: HotelIdDep, room_id: int, room_data: RoomAdd
) -> Any:
    await check_hotel_existence(db=db, hotel_id=room_data.hotel_id)

    result = await db.rooms.edit(room_data, id=room_id, hotel_id=hotel_id)
    await db.commit()
    if result == 404:
        raise HTTPException(status_code=404, detail="Номер не найден")
    return {"status": "OK"}


@router.patch(
    "/{room_id}",
    summary="Частично обновить данные номере в отеле",
    description="Позволяет обновить только некоторые поля номера в отеле",
)
async def partial_update_room(
    db: DBDep,
    hotel_id: HotelIdDep,
    room_id: int,
    room_data: RoomPatch,
):
    if room_data.hotel_id:
        await check_hotel_existence(db=db, hotel_id=room_data.hotel_id)

    result = await db.rooms.edit(
        room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id
    )
    await db.commit()
    if result == 404:
        raise HTTPException(status_code=404, detail="Номер не найден")
    return {"status": "OK"}


@router.delete("/{room_id}", summary="Удалить номер в отеле")
async def delete_room(db: DBDep, hotel_id: HotelIdDep, room_id: int):
    result = await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    if result == 404:
        raise HTTPException(status_code=404, detail="Номер не найден")
    return {"status": "OK"}
