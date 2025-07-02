from datetime import date

from fastapi import APIRouter, Body, Query
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.exceptions import (
    FacilityNotFoundException,
    FacilityNotFoundHTTPException,
    HotelNotFoundException,
    HotelNotFoundHTTPException,
    RoomAlreadyExistsException,
    RoomAlreadyExistsHTTPException,
    RoomPatchEmptyBodyException,
    RoomPatchEmptyBodyHTTPException,
    RoomToDeleteHasActiveBookingsException,
    RoomToDeleteHasActiveBookingsHTTPException,
    RoomNotFoundException,
    RoomNotFoundHTTPException,
)
from src.schemas.rooms import (
    Room,
    RoomAddRequest,
    RoomPatchRequest,
    RoomWithRels,
)
from src.services.rooms import RoomService

router = APIRouter(prefix="/hotels/{hotel_id}/rooms", tags=["Номера в отеле"])


@router.get(
    "/",
    summary="Получить список номеров отеля",
)
@cache(expire=10)
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(example="2025-06-19"),
    date_to: date = Query(example="2025-06-29"),
) -> list[RoomWithRels]:
    return await RoomService(db).get_filtered_by_time(hotel_id, date_from, date_to)


@router.get("/{room_id}", summary="Получить номер в отеле")
@cache(expire=10)
async def get_room(db: DBDep, hotel_id: int, room_id: int) -> RoomWithRels | None:
    try:
        return await RoomService(db).get_one_with_rels(room_id, hotel_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


@router.post("/", summary="Создать новый номер в отеле")
async def create_room(
    hotel_id: int,
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
    try:
        room = await RoomService(db).add_room(hotel_id, room_data)
        return {"status": "OK", "data": room}
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except FacilityNotFoundException:
        raise FacilityNotFoundHTTPException
    except RoomAlreadyExistsException:
        raise RoomAlreadyExistsHTTPException


@router.put("/{room_id}", summary="Обновить данные о номере в отеле")
async def update_room(
    db: DBDep, hotel_id: int, room_id: int, room_data: RoomAddRequest
) -> dict[str, str]:
    try:
        await RoomService(db).edit_room(hotel_id, room_id, room_data)
        return {"status": "OK"}
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except FacilityNotFoundException:
        raise FacilityNotFoundHTTPException


@router.patch(
    "/{room_id}",
    summary="Частично обновить данные номере в отеле",
    description="Позволяет обновить только некоторые поля номера в отеле",
)
async def partial_update_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room_data: RoomPatchRequest,
) -> dict[str, str]:
    try:
        await RoomService(db).partial_edit_room(hotel_id, room_id, room_data)
        return {"status": "OK"}
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except FacilityNotFoundException:
        raise FacilityNotFoundHTTPException
    except RoomPatchEmptyBodyException:
        raise RoomPatchEmptyBodyHTTPException


@router.delete("/{room_id}", summary="Удалить номер в отеле")
async def delete_room(db: DBDep, hotel_id: int, room_id: int) -> dict[str, str]:
    try:
        await RoomService(db).delete_room(hotel_id, room_id)
        return {"status": "OK"}
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except RoomToDeleteHasActiveBookingsException:
        raise RoomToDeleteHasActiveBookingsHTTPException
