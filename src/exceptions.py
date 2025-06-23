class ProxyException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, **kwargs)


class ObjectNotFoundException(ProxyException):
    detail = "Объект не найден"
