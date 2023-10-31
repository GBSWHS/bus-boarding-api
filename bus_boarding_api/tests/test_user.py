import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from bus_boarding_api.db.dao.user_dao import UserDAO
from bus_boarding_api.authentication import create_access_token


@pytest.mark.anyio
async def test_unauthorized_create_user(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("create_user")
    new_user = {
        "student_id": "3101",
        "name": "홍길동",
        "phone_number": "01012345678",
    }

    headers = {"Content-Type": "application/json"}
    response = await client.post(url, json=new_user, headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


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
    }

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


@pytest.mark.anyio
async def test_unauthorized_get_user(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("get_user", user_id=1)

    headers = {"Content-Type": "application/json"}
    response = await client.get(url, headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.anyio
async def test_get_user(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("get_user", user_id=1)

    user_dao = UserDAO(dbsession)
    await user_dao.create_super_user()
    access_token = create_access_token('1')
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    response = await client.get(url, headers=headers)
    assert response.status_code == status.HTTP_200_OK

    user = await user_dao.get(1)
    assert user.name == "_"


@pytest.mark.anyio
async def test_unauthorized_get_users(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("get_users")

    headers = {"Content-Type": "application/json"}
    response = await client.get(url, headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.anyio
async def test_get_users(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("get_users")

    user_dao = UserDAO(dbsession)
    await user_dao.create_super_user()
    access_token = create_access_token('1')
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    users = await user_dao.get_all(limit=100, offset=0)
    assert len(users) == 1


@pytest.mark.anyio
async def test_unauthorized_update_user(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("update_user", user_id=1)
    update_user = {
        "student_id": "3101",
        "name": "홍길동",
        "phone_number": "01012345678",
    }

    headers = {"Content-Type": "application/json"}
    response = await client.put(url, json=update_user, headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.anyio
async def test_unauthorized_delete_user(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("delete_user", user_id=1)

    headers = {"Content-Type": "application/json"}
    response = await client.delete(url, headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.anyio
async def test_delete_user(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("delete_user", user_id=1)

    user_dao = UserDAO(dbsession)
    await user_dao.create_super_user()
    access_token = create_access_token('1')
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    response = await client.delete(url, headers=headers)
    assert response.status_code == status.HTTP_200_OK

    saved_user = await user_dao.get(1)
    assert saved_user is None
