from typing import Any

from fastapi import APIRouter, HTTPException, Body

from src.api.dependencies import HotelIdDep, check_hotel_existence
from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import Room, RoomPATCH, RoomAdd

router = APIRouter(prefix="/{hotel_id}/rooms", tags=["Номера в отеле"])


@router.get(
    "/",
    summary="Получить список номеров отеля",
)
async def get_rooms(hotel_id: HotelIdDep) -> list[Room]:
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(hotel_id=hotel_id)


@router.get("/{room_id}", summary="Получить номер в отеле")
async def get_room(hotel_id: HotelIdDep, room_id: int) -> Room | None:
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(
            id=room_id, hotel_id=hotel_id
        )


@router.post("/", summary="Создать новый номер в отеле")
async def create_room(
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
    )
) -> dict[str, str | Room]:
    # не хочу отдельно hotel_id принимать как параметр функции, поэтому напрямую вызвал функцию из dependencies
    await check_hotel_existence(room_data.hotel_id)

    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(room_data)
        await session.commit()

    return {"status": "OK", "data": Room.model_validate(room)}


@router.put("/{room_id}", summary="Обновить данные о номере в отеле")
async def update_room(hotel_id: HotelIdDep, room_id: int, room_data: RoomAdd) -> Any:
    await check_hotel_existence(room_data.hotel_id)

    async with async_session_maker() as session:
        result = await RoomsRepository(session).edit(
            room_data, id=room_id, hotel_id=hotel_id
        )
        await session.commit()
    if result == 404:
        raise HTTPException(status_code=404, detail="Номер не найден")
    return {"status": "OK"}


@router.patch(
    "/{room_id}",
    summary="Частично обновить данные номере в отеле",
    description="Позволяет обновить только некоторые поля номера в отеле",
)
async def partial_update_room(
    hotel_id: HotelIdDep,
    room_id: int,
    room_data: RoomPATCH,
):
    if room_data.hotel_id:
        await check_hotel_existence(room_data.hotel_id)

    async with async_session_maker() as session:
        result = await RoomsRepository(session).edit(
            room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id
        )
        await session.commit()
    if result == 404:
        raise HTTPException(status_code=404, detail="Номер не найден")
    return {"status": "OK"}


@router.delete("/{room_id}", summary="Удалить номер в отеле")
async def delete_room(hotel_id: HotelIdDep, room_id: int):
    async with async_session_maker() as session:
        result = await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()
    if result == 404:
        raise HTTPException(status_code=404, detail="Номер не найден")
    return {"status": "OK"}
