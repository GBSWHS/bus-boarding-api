import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from bus_boarding_api.db.dao.user_dao import UserDAO
from bus_boarding_api.authentication import create_access_token


@pytest.mark.anyio
async def test_health(client: AsyncClient, fastapi_app: FastAPI) -> None:
    """
    Checks the health endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    """
    url = fastapi_app.url_path_for("health_check")
    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.anyio
async def test_create_user(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("create_user")
    new_user = {
        "student_id": "3101",
        "name": "홍길동",
        "phone_number": "01012345678",
        "year": 2023,
    }

    headers = {"Content-Type": "application/json"}
    response = await client.post(url, json=new_user, headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    user_dao = UserDAO(dbsession)
    await user_dao.create_super_user()
    access_token = create_access_token('1')
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    response = await client.post(url, json=new_user, headers=headers)
    assert response.status_code == status.HTTP_200_OK

    saved_new_user = await user_dao.get(2)
    assert saved_new_user.name == new_user.get("name")



