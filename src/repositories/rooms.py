from sqlalchemy import select

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsORM
from src.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsORM
    schema = Room

    async def get_all(
        self,
        hotel_id: int,
        *args,
        **kwargs,
    ) -> list[Room]:
        query = select(self.model).filter_by(hotel_id=hotel_id)
        result = await self.session.execute(query)
        return [
            Room.model_validate(room, from_attributes=True)
            for room in result.scalars().all()
        ]
