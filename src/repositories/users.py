from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from src.exceptions import UserNotFoundException
from src.models.users import UsersORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import (
    UserDataMapper,
    UserWithHashedPasswordDataMapper,
)
from src.schemas.users import UserWithHashedPasswordDTO


class UsersRepository(BaseRepository):
    model = UsersORM
    mapper = UserDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr) -> UserWithHashedPasswordDTO:
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        try:
            model = result.scalars().one()
        except NoResultFound:
            raise UserNotFoundException
        return UserWithHashedPasswordDataMapper.map_to_domain_entity(model)
