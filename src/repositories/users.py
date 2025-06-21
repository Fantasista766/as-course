from pydantic import EmailStr
from sqlalchemy import select

from src.models.users import UsersORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import (
    UserDataMapper,
    UserWithHashedPasswordDataMapper,
)


class UsersRepository(BaseRepository):
    model = UsersORM
    mapper = UserDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        return UserWithHashedPasswordDataMapper.map_to_domain_entity(model) if model else None
