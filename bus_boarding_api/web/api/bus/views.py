from typing import List

from fastapi import APIRouter
from fastapi.param_functions import Depends

from bus_boarding_api.db.dao.bus_dao import BusDAO
from bus_boarding_api.db.models.bus import BusModel
from bus_boarding_api.web.api.bus.schema import BusModelDTO, BusModelInputDTO, BusModelWithAllDTO, BusModelWithStopsDTO, BusModelWithRecordsDTO
from bus_boarding_api.authentication import PermissionChecker
from bus_boarding_api.permissions.models_permissions import Bus, BusStop, BoardingRecord

router = APIRouter()


@router.get("/{bus_id}",
            dependencies=[Depends(PermissionChecker([Bus.permissions.READ, BusStop.permissions.READ, BoardingRecord.permissions.READ]))],
            response_model=BusModelWithAllDTO)
async def get_bus(bus_id: int, bus_dao: BusDAO = Depends()) -> BusModel:
    fucking_bus_data = await bus_dao.get(
        bus_id=bus_id,
        load_stops=True,
        load_boarding_records=True,
    )
    print(fucking_bus_data.boarding_records)
    print(fucking_bus_data.bus_stops[0])
    return fucking_bus_data


@router.get("/{bus_id}/stops",
            dependencies=[Depends(PermissionChecker([Bus.permissions.READ, BusStop.permissions.READ]))],
            response_model=BusModelWithStopsDTO)
async def get_bus_stops(bus_id: int, bus_dao: BusDAO = Depends()) -> BusModel:
    return await bus_dao.get(
        bus_id=bus_id,
        load_stops=True,
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
    limit: int = 1000,
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
