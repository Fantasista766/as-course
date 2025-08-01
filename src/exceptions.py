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


class FileNotAnImageException(ArmorException):
    detail = "Файл не является изображением"


class HotelPatchEmptyBodyException(ArmorException):
    detail = "Необходимо указать хотя бы одно поле для обновления отеля"


class InvalidJWTException(ArmorException):
    detail = "Неверный токен"


class JWTMissingException(ArmorException):
    detail = "Токен отсутствует"


class PasswordTooShortException(ArmorException):
    detail = "Пароль слишком короткий"


class RoomPatchEmptyBodyException(ArmorException):
    detail = "Необходимо указать хотя бы одно поле для обновления номера"


class UserAlreadyLoggedOutException(ArmorException):
    detail = "Вы ещё не аутентифицированы"


class WrongPasswordException(ArmorException):
    detail = "Неверный пароль"


#########################################################################


class ObjectAlreadyExistsException(ArmorException):
    detail = "Объект уже существует"


class FacilityAlreadyExistsException(ObjectAlreadyExistsException):
    detail = "Удобство уже существует"


class HotelAlreadyExistsException(ObjectAlreadyExistsException):
    detail = "Отель уже существует"


class RoomAlreadyExistsException(ObjectAlreadyExistsException):
    detail = "Номер уже существует"


class UserAlreadyExistsException(ObjectAlreadyExistsException):
    detail = "Пользователь уже существует"


###############################################################


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


###########################################################################################


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


class FacilityAlreadyExistsHTTPException(ArmorHTTPException):
    status_code = 409
    detail = "Удобство уже существует"


class FacilityNotFoundHTTPException(ArmorHTTPException):
    status_code = 404
    detail = "Удобство не найдено"


class FileNotAnImageHTTPException(ArmorHTTPException):
    status_code = 422
    detail = "Файл не является изображением"


class HotelAlreadyExistsHTTPException(ArmorHTTPException):
    status_code = 409
    detail = "Отель уже существует"


class HotelPatchEmptyBodyHTTPException(ArmorHTTPException):
    status_code = 422
    detail = "Необходимо указать хотя бы одно поле для обновления отеля"


class HotelNotFoundHTTPException(ArmorHTTPException):
    status_code = 404
    detail = "Отель не найден"


class InvalidJWTHTTPException(ArmorHTTPException):
    status_code = 401
    detail = "Неверный токен"


class JWTMissingHTTPException(ArmorHTTPException):
    status_code = 401
    detail = "Токен отсутствует"


class PasswordTooShortHTTPException(ArmorHTTPException):
    status_code = 422
    detail = "Пароль слишком короткий"


class RoomAlreadyExistsHTTPException(ArmorHTTPException):
    status_code = 409
    detail = "Номер уже существует"


class RoomNotFoundHTTPException(ArmorHTTPException):
    status_code = 404
    detail = "Номер не найден"


class RoomPatchEmptyBodyHTTPException(ArmorHTTPException):
    status_code = 422
    detail = "Необходимо указать хотя бы одно поле для обновления номера"


class RoomToDeleteHasActiveBookingsHTTPException(ArmorException):
    status_code = 409
    detail = "Удаляемый номер имеет активные бронирования"


class UserAlreadyExistsHTTPException(ArmorHTTPException):
    status_code = 409
    detail = "Пользователь с таким email уже существует"


class UserAlreadyLoggedOutHTTPException(ArmorHTTPException):
    status_code = 409
    detail = "Вы ещё не аутентифицированы"


class UserNotFoundHTTPException(ArmorHTTPException):
    status_code = 404
    detail = "Пользователь не найден"


class WrongPasswordHTTPException(ArmorHTTPException):
    status_code = 401
    detail = "Неверный пароль"


def check_date_from_before_date_to(date_from: date, date_to: date) -> None:
    if date_from >= date_to:
        raise DateFromBeforeDateToHTTPException
