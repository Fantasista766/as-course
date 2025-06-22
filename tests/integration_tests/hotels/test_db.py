from src.schemas.hotels import HotelAdd
from src.utils.db_manager import DBManager


async def test_add_hotel(db: DBManager):
    hotel_data = HotelAdd(title="hotel 5 stars", location="Сочи")
    await db.hotels.add(hotel_data)
    await db.commit()
    new_hotels_data = await db.hotels.get_all()
    assert new_hotels_data[-1].title == hotel_data.title
    assert new_hotels_data[-1].location == hotel_data.location
