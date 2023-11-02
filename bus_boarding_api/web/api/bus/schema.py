from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BoardingRecordModelDTO(BaseModel):
    id: int
    user_id: int
    boarding_bus_id: int
    destination_stop_id: int
    time_created: datetime


class BusModelDTO(BaseModel):
    id: int
    name: str
    destination: int
    description: str

    model_config = ConfigDict(from_attributes=True)


# class BusModelWithAllDTO(BaseModel):
#     id: int
#     name: str
#     destination: int
#     description: str
#
#     bus_stops: List[BusStopModelDTO]
#     boarding_records: List[BoardingRecordModelDTO]


# class BusModelWithStopsDTO(BaseModel):
#     id: int
#     name: str
#     destination: int
#     description: str
#
#     bus_stop: BusStopModelDTO
#
#     model_config = ConfigDict(from_attributes=True)


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


class UserModelDTO(BaseModel):
    id: int
    student_id: str
    name: str
    phone_number: str
    role: str
