from datetime import date

from fastapi import HTTPException


class ArmorException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class AllRoomsAreBookedException(ArmorException):
    detail = "Не осталось свободных номеров"


class DateFromIsBeforeThanDateToException(ArmorException):
    detail = "Дата заезда не может быть позже даты выезда"


class ObjectAlreadyExistsException(ArmorException):
    detail = "Объект уже существует"


class ObjectNotFoundException(ArmorException):
    detail = "Объект не найден"


class ObjectToDeleteHasActiveRelations(ArmorException):
    detail = "Удаляемый объект используется в других таблицах"


class ArmorHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self, *args, **kwargs):
        super().__init__(self.status_code, self.detail, *args, **kwargs)


class HotelNotFoundHTTPException(ArmorHTTPException):
    status_code = 404
    detail = "Отель не найден"


class RoomNotFoundHTTPException(ArmorHTTPException):
    status_code = 404
    detail = "Номер не найден"


def check_date_from_before_date_to(date_from: date, date_to: date) -> None:
    if date_from >= date_to:
        raise HTTPException(status_code=422, detail=DateFromIsBeforeThanDateToException.detail)
