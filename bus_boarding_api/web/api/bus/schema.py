from typing import List

from pydantic import BaseModel, ConfigDict

from bus_boarding_api.web.api.bus_stop.schema import BusStopModelDTO
from bus_boarding_api.web.api.boarding_record.schema import BoardingRecordModelDTO


class BusModelDTO(BaseModel):
    id: int
    name: str
    destination: int
    description: str

    model_config = ConfigDict(from_attributes=True)


class BusModelWithAllDTO(BaseModel):
    id: int
    name: str
    destination: int
    description: str

    bus_stops: List[BusStopModelDTO]
    boarding_records: List[BoardingRecordModelDTO]

    # model_config = ConfigDict(from_attributes=True)


class BusModelWithStopsDTO(BaseModel):
    id: int
    name: str
    destination: int
    description: str

    bus_stop: BusStopModelDTO

    model_config = ConfigDict(from_attributes=True)


class BusModelWithRecordsDTO(BaseModel):
    id: int
    name: str
    destination: int
    description: str

    boarding_records: BoardingRecordModelDTO

    model_config = ConfigDict(from_attributes=True)


class BusModelInputDTO(BaseModel):
    name: str
    destination: int
    description: str
