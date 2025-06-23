class ProxyException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, **kwargs)


class AllRoomsAreBookedException(ProxyException):
    detail = "Не осталось свободных номеров"


class DateFromIsLaterThanDateToException(ProxyException):
    detail = "Дата заезда позже даты выезда"


class ObjectAlreadyExistsException(ProxyException):
    detail = "Объект уже существует"


class ObjectNotFoundException(ProxyException):
    detail = "Объект не найден"


class ObjectToDeleteHasActiveRelations(ProxyException):
    detail = "Удаляемый объект используется в других таблицах"
