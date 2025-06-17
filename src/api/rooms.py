from datetime import date
from typing import Any

from fastapi import APIRouter, HTTPException, Body, Query

from src.api.dependencies import (
    DBDep,
    HotelIdDep,
)
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import (
    Room,
    RoomAdd,
    RoomAddRequest,
    RoomPatch,
    RoomPatchRequest,
    RoomWithRels,
)

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
) -> list[RoomWithRels]:
    return await db.rooms.get_filtered_by_time(
        hotel_id=hotel_id, date_from=date_from, date_to=date_to
    )


@router.get("/{room_id}", summary="Получить номер в отеле")
async def get_room(db: DBDep, hotel_id: HotelIdDep, room_id: int) -> Room | None:
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/", summary="Создать новый номер в отеле")
async def create_room(
    hotel_id: HotelIdDep,
    db: DBDep,
    room_data: RoomAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Luxury",
                "value": {
                    "title": "Анаконда",
                    "description": "Всё включено",
                    "price": 1000,
                    "quantity": 10,
                    "facilities_ids": [],
                },
            },
            "2": {
                "summary": "Basic",
                "value": {
                    "title": "Кобра",
                    "description": "Основные удобства",
                    "price": 300,
                    "quantity": 50,
                    "facilities_ids": [],
                },
            },
        }
    ),
) -> dict[str, str | Room]:
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)

    if room_data.facilities_ids:
        rooms_facilities_data = [
            RoomFacilityAdd(room_id=room.id, facility_id=f_id)
            for f_id in room_data.facilities_ids
        ]
        res = await db.rooms_facilities.add_batch(rooms_facilities_data)  # type: ignore
        if not res:
            raise HTTPException(status_code=404, detail="Удобства не найдены")
    await db.commit()

    return {"status": "OK", "data": Room.model_validate(room)}


@router.put("/{room_id}", summary="Обновить данные о номере в отеле")
async def update_room(
    db: DBDep, hotel_id: HotelIdDep, room_id: int, room_data: RoomAddRequest
) -> Any:
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())

    result = await db.rooms.edit(_room_data, id=room_id, hotel_id=hotel_id)
    if result == 404:
        raise HTTPException(status_code=404, detail="Номер не найден")
    if room_data.facilities_ids:
        await db.rooms_facilities.set_room_facilities(
            room_id, facilities_ids=room_data.facilities_ids
        )

    await db.commit()
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
    room_data: RoomPatchRequest,
):
    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)

    result = await db.rooms.edit(
        _room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id
    )
    if result == 404:
        raise HTTPException(status_code=404, detail="Номер не найден")

    if room_data.facilities_ids:
        await db.rooms_facilities.set_room_facilities(
            room_id, facilities_ids=room_data.facilities_ids
        )

    await db.commit()

    return {"status": "OK"}


@router.delete("/{room_id}", summary="Удалить номер в отеле")
async def delete_room(db: DBDep, hotel_id: HotelIdDep, room_id: int):
    result = await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    if result == 404:
        raise HTTPException(status_code=404, detail="Номер не найден")
    return {"status": "OK"}
