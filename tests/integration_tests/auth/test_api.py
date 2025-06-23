from httpx import AsyncClient
import pytest


@pytest.mark.parametrize(
    "email, password, first_name, last_name, status_code",
    [
        ("kot@pes.com", "1234", "A", "B", 409),
        ("kot123@pes.com", "1234", "A", "B", 200),
        ("dfasdf@pes.com", "1342sdfaef234", "Alna", "Bumaye", 200),
        ("kotcom", "1234", "A", "B", 422),
    ],
)
async def test_auth_flow(
    email: str,
    password: str,
    first_name: str,
    last_name: str,
    status_code: int,
    ac: AsyncClient,
):
    # 1. Регистрация
    response = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
        },
    )
    assert response.status_code == status_code
    if status_code != 200:
        return

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
    response = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )
    assert response.status_code == 200
    assert "access_token" in ac.cookies
    assert "access_token" in response.json()

    # 3. Получение инфы о пользователе
    response = await ac.get("/auth/me")
    user = response.json()
    assert response.status_code == 200
    assert user["email"] == email
    assert user["first_name"] == first_name
    assert user["last_name"] == last_name
    assert "id" in user
    assert "password" not in user
    assert "hashed_password" not in user

    # 4. Выход из системы
    await ac.post("/auth/logout")
    assert "access_token" not in ac.cookies

    # 5. Получение инфы о пользователе, не находясь в системе
    response = await ac.get("/auth/me")
    assert response.status_code == 401
