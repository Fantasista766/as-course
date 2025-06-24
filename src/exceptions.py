from datetime import date

from fastapi import HTTPException


class ArmorException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class AllRoomsAreBookedException(ArmorException):
    detail = "Не осталось свободных номеров"


class DateFromBeforeDateToException(ArmorException):
    detail = "Дата заезда не может быть позже даты выезда"


class InvalidJWTException(ArmorException):
    detail = "Неверный токен"


class JWTMissingException(ArmorException):
    detail = "Токен отсутствует"


class ObjectAlreadyExistsException(ArmorException):
    detail = "Объект уже существует"


class UserAlreadyExistsException(ObjectAlreadyExistsException):
    detail = "Пользователь уже существует"


class ObjectNotFoundException(ArmorException):
    detail = "Объект не найден"


class FacilityNotFoundException(ObjectNotFoundException):
    detail = "Удобство не найдено"


class HotelNotFoundException(ObjectNotFoundException):
    detail = "Отель не найден"


class RoomNotFoundException(ObjectNotFoundException):
    detail = "Номер не найден"


class UserNotFoundException(ObjectNotFoundException):
    detail = "Пользователь не найден"


class ObjectToDeleteHasActiveRelationsException(ArmorException):
    detail = "Удаляемый объект имеет активные связи с другими таблицами"


class RoomToDeleteHasActiveBookingsException(ObjectToDeleteHasActiveRelationsException):
    detail = "Номер имеет активные бронирования"


class WrongPasswordException(ArmorException):
    detail = "Неверный пароль"


class ArmorHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self, *args, **kwargs):
        super().__init__(self.status_code, self.detail, *args, **kwargs)


class AllRoomsAreBookedHTTPException(ArmorHTTPException):
    status_code = 409
    detail = "Не осталось свободных номеров"


class DateFromBeforeDateToHTTPException(ArmorHTTPException):
    status_code = 422
    detail = "Дата заезда не может быть позже даты выезда"


class FacilityNotFoundHTTPException(ArmorHTTPException):
    status_code = 404
    detail = "Удобство не найдено"


class HotelNotFoundHTTPException(ArmorHTTPException):
    status_code = 404
    detail = "Отель не найден"


class InvalidJWTHTTPException(ArmorHTTPException):
    status_code = 401
    detail = "Неверный токен"


class JWTMissingHTTPException(ArmorHTTPException):
    status_code = 401
    detail = "Токен отсутствует"


class RoomToDeleteHasActiveBookingsHTTPException(ArmorException):
    status_code = 409
    detail = "Удаляемый номер имеет активные бронирования"


class RoomNotFoundHTTPException(ArmorHTTPException):
    status_code = 404
    detail = "Номер не найден"


class UserAlreadyExistsHTTPException(ArmorHTTPException):
    status_code = 409
    detail = "Пользователь с таким email уже существует"


class UserNotFoundHTTPException(ArmorHTTPException):
    status_code = 404
    detail = "Пользователь не найден"


class WrongPasswordHTTPException(ArmorHTTPException):
    status_code = 401
    detail = "Неверный пароль"


def check_date_from_before_date_to(date_from: date, date_to: date) -> None:
    if date_from >= date_to:
        raise DateFromBeforeDateToHTTPException
