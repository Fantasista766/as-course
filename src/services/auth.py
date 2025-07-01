from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import Request, Response
from passlib.context import CryptContext
import jwt

from src.config import settings
from src.exceptions import (
    JWTMissingException,
    InvalidJWTException,
    ObjectAlreadyExistsException,
    ObjectNotFoundException,
    PasswordTooShortException,
    UserAlreadyExistsException,
    UserNotFoundException,
    WrongPasswordException,
)
from src.schemas.users import UserAdd, UserLogin, UserRegister
from src.services.base import BaseService


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def register_user(self, user_data: UserRegister) -> None:
        if len(user_data.password) < 8:
            raise PasswordTooShortException
        hashed_password = self.hash_password(user_data.password)
        new_user_data = UserAdd(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            hashed_password=hashed_password,
        )
        try:
            await self.db.users.add(new_user_data)  # type: ignore
        except ObjectAlreadyExistsException:
            raise UserAlreadyExistsException

        await self.db.commit()  # type: ignore

    async def login_user(self, user_data: UserLogin) -> str:
        try:
            user = await self.db.users.get_user_with_hashed_password(email=user_data.email)  # type: ignore
            self.verify_password(user_data.password, user.hashed_password)
            return self.create_access_token({"user_id": user.id})
        except ObjectNotFoundException:
            raise UserNotFoundException

    async def get_user(self, user_id: int) -> str:
        return await self.db.users.get_one(id=user_id)  # type: ignore

    async def logout_user(self, response: Response) -> None:
        response.delete_cookie("access_token")

    def get_token(self, request: Request) -> str:
        try:
            return request.cookies["access_token"]
        except KeyError:
            raise JWTMissingException

    def create_access_token(self, data: dict[str, Any]) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode |= {"exp": expire}
        encoded_jwt = jwt.encode(  # type: ignore
            to_encode, key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> None:
        if not self.pwd_context.verify(plain_password, hashed_password):
            raise WrongPasswordException

    def decode_token(self, token: str) -> dict[str, Any]:
        try:
            return jwt.decode(token, key=settings.JWT_SECRET_KEY, algorithms=settings.JWT_ALGORITHM)  # type: ignore
        except jwt.exceptions.DecodeError as _:
            raise InvalidJWTException
