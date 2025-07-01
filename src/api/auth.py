from fastapi import APIRouter, Response
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import (
    InvalidJWTException,
    InvalidJWTHTTPException,
    PasswordTooShortException,
    PasswordTooShortHTTPException,
    UserAlreadyExistsException,
    UserAlreadyExistsHTTPException,
    UserNotFoundException,
    UserNotFoundHTTPException,
    WrongPasswordException,
    WrongPasswordHTTPException,
)
from src.schemas.users import UserRegister, UserLogin
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register", summary="Регистрация пользователя")
async def register_user(
    db: DBDep,
    user_data: UserRegister,
) -> dict[str, str]:
    try:
        await AuthService(db).register_user(user_data)
        return {"status": "OK"}
    except PasswordTooShortException:
        raise PasswordTooShortHTTPException
    except UserAlreadyExistsException:
        raise UserAlreadyExistsHTTPException


@router.post("/login", summary="Аутентификация пользователя")
async def login_user(
    db: DBDep,
    user_data: UserLogin,
    response: Response,
) -> dict[str, str]:
    try:
        access_token = await AuthService(db).login_user(user_data)
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}
    except InvalidJWTException:
        raise InvalidJWTHTTPException
    except UserNotFoundException:
        raise UserNotFoundHTTPException
    except WrongPasswordException:
        raise WrongPasswordHTTPException


@router.post("/logout")
async def logout_user(response: Response):
    await AuthService().logout_user(response)
    return {"status": "OK"}


@router.get("/me")
@cache(expire=10)
async def get_me(db: DBDep, user_id: UserIdDep):
    try:
        return await AuthService(db).get_user(user_id)
    except UserNotFoundException:
        raise UserNotFoundHTTPException
