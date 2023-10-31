from typing import List

import pyotp
from fastapi import APIRouter, HTTPException
from fastapi.param_functions import Depends

from bus_boarding_api.authentication import (authenticate_user, authenticate_admin,
                                             create_access_token, get_current_user)
from bus_boarding_api.db.dao.user_dao import UserDAO
from bus_boarding_api.db.models.user import UserModel
from bus_boarding_api.authentication import PermissionChecker
from bus_boarding_api.permissions.models_permissions import User
from bus_boarding_api.web.api.user.schema import (UserModelDTO, UserModelInputDTO,
                                                  TokenDTO, AuthenticateInputDTO)

router = APIRouter()


@router.get("/me", dependencies=[Depends(PermissionChecker([]))],
            response_model=UserModelDTO)
async def get_me(
    user: UserModel = Depends(get_current_user),
    user_dao: UserDAO = Depends(),
) -> UserModel:

    return await user_dao.get(user_id=user.id)


@router.get("/{user_id}")
async def get_user(
    user_id: int,
    user_dao: UserDAO = Depends(),
) -> None:

    await user_dao.get(user_id=user_id)


@router.get("/",
            dependencies=[Depends(PermissionChecker([User.permissions.READ]))],
            response_model=List[UserModelDTO])
async def get_users(
    limit: int = 1000,
    offset: int = 0,
    user_dao: UserDAO = Depends(),
) -> List[UserModel]:

    return await user_dao.get_all(limit=limit, offset=offset)


@router.post("/", dependencies=[Depends(PermissionChecker([User.permissions.CREATE]))],)
async def create_user(
    new_user: UserModelInputDTO,
    user_dao: UserDAO = Depends(),
) -> None:

    await user_dao.create(
        student_id=new_user.student_id,
        name=new_user.name,
        phone_number=new_user.phone_number,
        bus_id=new_user.boarding_bus_id,
        stop_id=new_user.destination_stop_id,
    )


@router.delete("/{user_id}",
               dependencies=[Depends(PermissionChecker([User.permissions.DELETE]))])
async def delete_user(
    user_id: int,
    user_dao: UserDAO = Depends(),
) -> None:

    await user_dao.delete(user_id=user_id)


@router.post("/login", response_model=TokenDTO)
async def login(form_data: AuthenticateInputDTO, user_dao: UserDAO = Depends()):
    base32_string = pyotp.random_base32()

    if form_data.password and form_data.password == "dummy":
        user = await authenticate_user(
            student_id=form_data.student_id,
            name=form_data.name,
            phone_number=form_data.phone_number,
            user_dao=user_dao
        )
    else:
        user = await authenticate_admin(student_id=form_data.password, user_dao=user_dao)

    if not user:
        raise HTTPException(status_code=401, detail="일치하지 않는 정보입니다")

    access_token = create_access_token(data=user.id)
    await user_dao.update_totp_secret(user_id=user.id, totp_secret=base32_string)

    return {
        "access_token": access_token,
        "totp_secret": base32_string,
        "type": user.role,
    }
