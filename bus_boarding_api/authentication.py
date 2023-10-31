from typing import List
from datetime import datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

from bus_boarding_api.permissions.base import ModelPermission
from bus_boarding_api.permissions.roles import get_role_permissions
from bus_boarding_api.settings import settings
from bus_boarding_api.db.models.user import UserModel
from bus_boarding_api.db.dao.user_dao import UserDAO


class BearAuthException(Exception):
    pass


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: str):
    to_encode = {"id": data}
    expire = datetime.utcnow() + timedelta(hours=settings.auth_expire_hours)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.auth_secret, algorithm=settings.auth_algorithm)
    return encoded_jwt


def get_token_payload(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.auth_secret, algorithms=[settings.auth_algorithm])
        payload_sub: str = payload.get("id")

        if payload_sub is None:
            raise BearAuthException("Token could not be validated")
        return payload_sub
    except JWTError as e:
        print(e)
        raise BearAuthException("Token could not be validated")


async def authenticate_user(student_id: str, name: str, phone_number: str, user_dao: UserDAO = Depends()) -> UserModel:
    user = await user_dao.get_by_infos(
        student_id=student_id,
        name=name,
        phone_number=phone_number
    )

    return user


async def authenticate_admin(student_id: str, user_dao: UserDAO = Depends()) -> UserModel:
    user = await user_dao.get_by_password(password=student_id)

    return user


async def get_current_user(token: str = Depends(oauth2_scheme), user_dao: UserDAO = Depends()):
    try:
        user_id = get_token_payload(token)
    except BearAuthException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate bearer token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user = await user_dao.get(user_id=(int(user_id)))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized, could not validate credentials.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user


class PermissionChecker:
    def __init__(self, permissions_required: List[ModelPermission]) -> object:
        self.permissions_required = permissions_required

    def __call__(self, user: UserModel = Depends(get_current_user)):
        for permission_required in self.permissions_required:
            if permission_required not in get_role_permissions(user.role):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not enough permissions to access this resource")
        return user
