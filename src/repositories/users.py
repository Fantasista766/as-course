from pydantic import EmailStr
from sqlalchemy import select

from src.models.users import UsersORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import (
    UserDataMapper,
    UserWithHashedPasswordDataMapper,
)
from src.schemas.users import UserWithHashedPassword


class UsersRepository(BaseRepository):
    model = UsersORM
    mapper = UserDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr) -> UserWithHashedPassword:
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one()
        return UserWithHashedPasswordDataMapper.map_to_domain_entity(model)
