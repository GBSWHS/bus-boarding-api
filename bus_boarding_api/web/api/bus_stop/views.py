from typing import List

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from bus_boarding_api.db.dao.bus_stop_dao import BusStopDAO
from bus_boarding_api.db.dependencies import get_db_session
from bus_boarding_api.db.models.bus_stop import BusStopModel
from bus_boarding_api.web.api.bus_stop.schema import BusStopModelDTO, BusStopModelInputDTO
from bus_boarding_api.authentication import PermissionChecker
from bus_boarding_api.permissions.models_permissions import BusStop

router = APIRouter()


@router.get("", dependencies=[Depends(PermissionChecker([BusStop.permissions.READ]))], response_model=List[BusStopModelDTO])
async def get_bus_stops(db: AsyncSession = Depends(get_db_session)) -> List[BusStopModel]:
    bus_stop_dao = BusStopDAO(db)

    return await bus_stop_dao.get_all(limit=1000, offset=0)


@router.get("/{bus_stop_id}", dependencies=[Depends(PermissionChecker([BusStop.permissions.READ]))], response_model=BusStopModelDTO)
async def get_bus_stops_by_id(bus_stop_id: int, db: AsyncSession = Depends(get_db_session)) -> BusStopModel:
    bus_stop_dao = BusStopDAO(db)

    return await bus_stop_dao.get(bus_stop_id)


@router.post("", dependencies=[Depends(PermissionChecker([BusStop.permissions.CREATE]))],)
async def create_bus_stop(
    new_bus_stop: BusStopModelInputDTO, db: AsyncSession = Depends(get_db_session)
) -> None:
    bus_stop_dao = BusStopDAO(db)

    await bus_stop_dao.create(
        bus_id=new_bus_stop.bus_id,
        order=new_bus_stop.order,
        name=new_bus_stop.name
    )


@router.delete("/{bus_stop_id}",
               dependencies=[Depends(PermissionChecker([BusStop.permissions.DELETE]))])
async def delete_bus_stop(
    bus_stop_id: int, db: AsyncSession = Depends(get_db_session)
) -> None:
    bus_stop_dao = BusStopDAO(db)

    await bus_stop_dao.delete(bus_stop_id=bus_stop_id)
