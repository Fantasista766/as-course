from httpx import AsyncClient


async def test_get_hotels(ac: AsyncClient):
    response = await ac.get("/hotels", params={"date_from": "2025-06-21", "date_to": "2025-06-28"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
