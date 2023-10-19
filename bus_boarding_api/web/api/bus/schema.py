from pydantic import BaseModel, ConfigDict

from bus_boarding_api.web.api.bus_stop.schema import BusStopModelDTO
from bus_boarding_api.web.api.boarding_info.schema import BoardingInfoModelDTO
from bus_boarding_api.web.api.boarding_record.schema import BoardingRecordModelDTO


class BusModelDTO(BaseModel):
    id: int
    name: str
    destination: str
    description: str

    model_config = ConfigDict(from_attributes=True)


class BusModelWithAllDTO(BaseModel):
    id: int
    name: str
    destination: str
    description: str

    bus_stop: BusStopModelDTO
    boarding_infos: BoardingInfoModelDTO
    boarding_records: BoardingRecordModelDTO

    model_config = ConfigDict(from_attributes=True)


class BusModelWithStopsDTO(BaseModel):
    id: int
    name: str
    destination: str
    description: str

    bus_stop: BusStopModelDTO

    model_config = ConfigDict(from_attributes=True)


class BusModelWithInfosDTO(BaseModel):
    id: int
    name: str
    destination: str
    description: str

    boarding_infos: BoardingInfoModelDTO

    model_config = ConfigDict(from_attributes=True)


class BusModelWithRecordsDTO(BaseModel):
    id: int
    name: str
    destination: str
    description: str

    boarding_records: BoardingRecordModelDTO

    model_config = ConfigDict(from_attributes=True)


class BusModelInputDTO(BaseModel):
    name: str
    destination: str
    description: str
