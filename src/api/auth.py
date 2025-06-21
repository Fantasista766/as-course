from fastapi import APIRouter, HTTPException, Response
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.users import UserAdd, UserRegister, UserLogin
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register", summary="Регистрация пользователя")
async def register_user(
    db: DBDep,
    user_data: UserRegister,
):
    hashed_password = AuthService().hash_password(user_data.password)
    new_user_data = UserAdd(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        hashed_password=hashed_password,
    )
    res = await db.users.add(new_user_data)
    await db.commit()

    if not res:
        raise HTTPException(
            status_code=400, detail="Пользователь с таким email уже зарегистрирован"
        )

    return {"status": "OK"}


@router.post("/login", summary="Аутентификация пользователя")
async def login_user(
    db: DBDep,
    user_data: UserLogin,
    response: Response,
):
    user = await db.users.get_user_with_hashed_password(email=user_data.email)
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован")
    if not AuthService().verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Пароль неверный")

    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}


@router.get("/me")
@cache(expire=10)
async def get_me(db: DBDep, user_id: UserIdDep):
    user = await db.users.get_one_or_none(id=user_id)
    return user
