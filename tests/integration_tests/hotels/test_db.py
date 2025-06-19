from src.database import async_session_maker_null_pool
from src.schemas.hotels import HotelAdd
from src.utils.db_manager import DBManager


async def test_add_hotel():
    hotel_data = HotelAdd(title="hotel 5 stars", location="Сочи")
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        await db.hotels.add(hotel_data)
        await db.commit()
        new_hotels_data = await db.hotels.get_all()
        assert new_hotels_data[0].title == hotel_data.title  # type: ignore
        assert new_hotels_data[0].location == hotel_data.location  # type: ignore
        assert len(new_hotels_data) == 1
