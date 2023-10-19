from typing import List

from fastapi import APIRouter
from fastapi.param_functions import Depends

from bus_boarding_api.db.dao.bus_dao import BusDAO
from bus_boarding_api.db.models.bus import BusModel
from bus_boarding_api.web.api.bus.schema import BusModelDTO, BusModelInputDTO, BusModelWithAllDTO, BusModelWithStopsDTO, BusModelWithInfosDTO, BusModelWithRecordsDTO
from bus_boarding_api.authentication import PermissionChecker
from bus_boarding_api.permissions.models_permissions import Bus, BusStop, BoardingInfo, BoardingRecord

router = APIRouter()


@router.get("/{bus_id}",
            dependencies=[Depends(PermissionChecker([Bus.permissions.READ, BusStop.permissions.READ, BoardingInfo.permissions.READ, BoardingRecord.permissions.READ]))],
            response_model=BusModelWithAllDTO)
async def get_bus(bus_id: int, bus_dao: BusDAO = Depends()) -> BusModel:
    return await bus_dao.get(
        bus_id=bus_id,
        load_stops=True,
        load_boarding_infos=True,
        load_boarding_records=True,
    )


@router.get("/{bus_id}/stops",
            dependencies=[Depends(PermissionChecker([Bus.permissions.READ, BusStop.permissions.READ]))],
            response_model=BusModelWithStopsDTO)
async def get_bus_stops(bus_id: int, bus_dao: BusDAO = Depends()) -> BusModel:
    return await bus_dao.get(
        bus_id=bus_id,
        load_stops=True,
    )


@router.get("/{bus_id}/infos",
            dependencies=[Depends(PermissionChecker([Bus.permissions.READ, BoardingInfo.permissions.READ]))],
            response_model=BusModelWithInfosDTO)
async def get_bus_infos(bus_id: int, bus_dao: BusDAO = Depends()) -> BusModel:
    return await bus_dao.get(
        bus_id=bus_id,
        load_boarding_infos=True,
    )


@router.get("/{bus_id}/records",
            dependencies=[Depends(PermissionChecker([Bus.permissions.READ, BoardingRecord.permissions.READ]))],
            response_model=BusModelWithRecordsDTO)
async def get_bus_records(bus_id: int, bus_dao: BusDAO = Depends()) -> BusModel:
    return await bus_dao.get(
        bus_id=bus_id,
        load_boarding_records=True,
    )


@router.get("/",
            dependencies=[Depends(PermissionChecker([Bus.permissions.READ]))],
            response_model=List[BusModelDTO])
async def get_buses(
    limit: int = 50,
    offset: int = 0,
    bus_dao: BusDAO = Depends(),
) -> List[BusModel]:

    return await bus_dao.get_all(limit=limit, offset=offset)


@router.post("/", dependencies=[Depends(PermissionChecker([Bus.permissions.CREATE]))],)
async def create_bus(
    new_bus: BusModelInputDTO,
    bus_dao: BusDAO = Depends(),
) -> None:

    await bus_dao.create(
        name=new_bus.name,
        destination=new_bus.destination,
        description=new_bus.description
    )


@router.delete("/{bus_id}",
               dependencies=[Depends(PermissionChecker([Bus.permissions.DELETE]))])
async def delete_bus(
    bus_id: int,
    bus_dao: BusDAO = Depends(),
) -> None:

    await bus_dao.delete(bus_id=bus_id)
