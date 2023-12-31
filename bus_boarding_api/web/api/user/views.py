from typing import List

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from bus_boarding_api.authentication import get_current_user
from bus_boarding_api.db.dao.user_dao import UserDAO
from bus_boarding_api.db.dependencies import get_db_session
from bus_boarding_api.db.models.boarding_record import BoardingRecordModel
from bus_boarding_api.db.models.user import UserModel
from bus_boarding_api.authentication import PermissionChecker
from bus_boarding_api.permissions.models_permissions import User
from bus_boarding_api.web.api.user.schema import UserModelDTO, UserModelInputDTO

router = APIRouter()


@router.get("/me", dependencies=[Depends(PermissionChecker([]))],
            response_model=UserModelDTO)
async def get_me(
    user: UserModel = Depends(get_current_user), db: AsyncSession = Depends(get_db_session)
) -> UserModel:
    user_dao = UserDAO(db)

    return await user_dao.get(user_id=user.id)


@router.get("/me/records", dependencies=[Depends(PermissionChecker([]))],
            response_model=List[UserModelDTO])
async def get_me_records(
    limit: int = 10,
    user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
) -> List[BoardingRecordModel]:
    user_dao = UserDAO(db)

    return await user_dao.get_all_records(user_id=user.id, limit=limit)


@router.get("/{user_id}", dependencies=[Depends(PermissionChecker([User.permissions.READ]))],
            response_model=UserModelDTO)
async def get_user(
    user_id: int, db: AsyncSession = Depends(get_db_session)
) -> UserModel:
    user_dao = UserDAO(db)

    return await user_dao.get(user_id=user_id)


@router.get("",
            dependencies=[Depends(PermissionChecker([User.permissions.READ]))],
            response_model=List[UserModelDTO])
async def get_users(
    limit: int = 1000,
    offset: int = 0,
    db: AsyncSession = Depends(get_db_session)
) -> List[UserModel]:
    user_dao = UserDAO(db)

    return await user_dao.get_all(limit=limit, offset=offset)


@router.post("", dependencies=[Depends(PermissionChecker([User.permissions.CREATE]))],)
async def create_user(
    new_user: UserModelInputDTO,
    db: AsyncSession = Depends(get_db_session)
) -> None:
    user_dao = UserDAO(db)

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
    user_id: int, db: AsyncSession = Depends(get_db_session)
) -> None:
    user_dao = UserDAO(db)

    await user_dao.delete(user_id=user_id)
