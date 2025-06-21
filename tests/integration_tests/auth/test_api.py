from httpx import AsyncClient
import pytest


@pytest.mark.parametrize(
    "email, password, first_name, last_name",
    [
        ("kot123@pes.com", "1234", "A", "B"),
        ("dfasdf@pes.com", "1342sdfaef234", "Alna", "Bumaye"),
    ],
)
async def test_auth_flow(
    email: str, password: str, first_name: str, last_name: str, ac: AsyncClient
):
    # 1. Регистрация
    user_data = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
        },
    )
    assert user_data.status_code == 200

    # 2. Логин
    # 2.1 Неуспешный
    response = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password + "!",
        },
    )
    assert response.status_code == 401
    # 2.2 Успешный
    await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )
    assert "access_token" in ac.cookies

    # 3. Получение инфы о пользователе
    response = await ac.get("/auth/me")
    user = response.json()
    assert user["email"] == email
    assert user["first_name"] == first_name
    assert user["last_name"] == last_name

    # 4. Выход из системы
    await ac.post("/auth/logout")
    assert "access_token" not in ac.cookies

    # 5. Получение инфы о пользователе, не находясь в системе
    response = await ac.get("/auth/me")
    assert response.status_code == 401
