from src.repositories.base import BaseRepository
from src.models.hotels import HotelsORM


class HotelsRepository(BaseRepository):
    model = HotelsORM
