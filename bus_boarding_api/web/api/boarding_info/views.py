from typing import List

from fastapi import APIRouter
from fastapi.param_functions import Depends

from bus_boarding_api.db.dao.boarding_info_dao import BoardingInfoDAO
from bus_boarding_api.db.models.user import UserModel
from bus_boarding_api.db.models.bus_stop import BusStopModel
from bus_boarding_api.web.api.boarding_info.schema import BoardingInfoModelInputDTO
from bus_boarding_api.authentication import PermissionChecker, get_current_user
from bus_boarding_api.permissions.models_permissions import BoardingInfo

router = APIRouter()


@router.post("/", dependencies=[Depends(PermissionChecker([BoardingInfo.permissions.CREATE]))],)
async def create_boarding_info(
    new_boarding_info: BoardingInfoModelInputDTO,
    boarding_info_dao: BoardingInfoDAO = Depends(),
    user: UserModel = Depends(get_current_user)
) -> None:

    await boarding_info_dao.create(
        user_id=user.id,
        bus_id=new_boarding_info.bus_id,
        destination_stop_id=new_boarding_info.destination_stop_id
    )


@router.patch("/", dependencies=[Depends(PermissionChecker([BoardingInfo.permissions.UPDATE]))],)
async def update_boarding_info(
    new_boarding_info: BoardingInfoModelInputDTO,
    boarding_info_dao: BoardingInfoDAO = Depends(),
    user: UserModel = Depends(get_current_user)
) -> None:

    await boarding_info_dao.create(
        user_id=user.id,
        bus_id=new_boarding_info.bus_id,
        destination_stop_id=new_boarding_info.destination_stop_id
    )


@router.delete("/{bus_stop_id}",
               dependencies=[Depends(PermissionChecker([BusStop.permissions.DELETE]))])
async def delete_bus_stop(
    bus_stop_id: int,
    bus_stop_dao: BusStopDAO = Depends(),
) -> None:

    await bus_stop_dao.delete(bus_stop_id=bus_stop_id)
