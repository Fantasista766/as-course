from datetime import date

from fastapi import HTTPException


class ArmormException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class AllRoomsAreBookedException(ArmormException):
    detail = "Не осталось свободных номеров"


class DateFromIsBeforeThanDateToException(ArmormException):
    detail = "Дата заезда не может быть позже даты выезда"


class ObjectAlreadyExistsException(ArmormException):
    detail = "Объект уже существует"


class ObjectNotFoundException(ArmormException):
    detail = "Объект не найден"


class ObjectToDeleteHasActiveRelations(ArmormException):
    detail = "Удаляемый объект используется в других таблицах"


def check_date_from_before_date_to(date_from: date, date_to: date) -> None:
    if date_from >= date_to:
        raise DateFromIsBeforeThanDateToException


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
