from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.param_functions import Depends

from bus_boarding_api.authentication import authenticate_user, create_access_token
from bus_boarding_api.db.dao.user_dao import UserDAO
from bus_boarding_api.db.models.user import UserModel
from bus_boarding_api.authentication import PermissionChecker
from bus_boarding_api.permissions.models_permissions import User, BoardingInfo
from bus_boarding_api.web.api.user.schema import (UserModelDTO, UserModelInputDTO,
                                                  TokenDTO, AuthenticateInputDTO)

router = APIRouter()


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
    year: int = datetime.now().year,
    limit: int = 50,
    offset: int = 0,
    user_dao: UserDAO = Depends(),
) -> List[UserModel]:

    return await user_dao.get_all(year=year, limit=limit, offset=offset)


@router.post("/", dependencies=[Depends(PermissionChecker([User.permissions.CREATE, BoardingInfo.permissions.CREATE]))],)
async def create_user(
    new_user: UserModelInputDTO,
    user_dao: UserDAO = Depends(),
) -> None:

    await user_dao.create(
        student_id=new_user.student_id,
        name=new_user.name,
        phone_number=new_user.phone_number,
        year=new_user.year,
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
    user = await authenticate_user(
        student_id=form_data.student_id,
        name=form_data.name,
        phone_number=form_data.phone_number,
        user_dao=user_dao
    )
    if not user:
        raise HTTPException(status_code=401, detail="Invalid info")

    access_token = create_access_token(data=user.id)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
