from fastapi import HTTPException, status


class PekarnaException(HTTPException):  # <-- наследуемся от HTTPException, который наследован от Exception
    status_code = 500  # <-- задаем значения по умолчанию
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(PekarnaException):  # <-- обязательно наследуемся от нашего класса
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class IncorrectUsernameOrPassword(PekarnaException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Не правильный пароль или email"


class TokenExpireException(PekarnaException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токет истек"


class TokenAbsen(PekarnaException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class IncorrectTokenFormant(PekarnaException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Не корректный формат токена"


class UserIsNotID(PekarnaException):
    status_code = status.HTTP_401_UNAUTHORIZED

class Noactive(PekarnaException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Юзер не активный"

