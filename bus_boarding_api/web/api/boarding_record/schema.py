from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserModelDTO(BaseModel):
    id: int
    student_id: str
    name: str
    phone_number: str

    model_config = ConfigDict(from_attributes=True)


class JoinedUserModelDTO(BaseModel):
    class BusModelDTO(BaseModel):
        id: int
        name: str
        destination: int
        description: str

    class BusStopModelDTO(BaseModel):
        id: int
        name: str
        location: str

    id: int
    student_id: str
    name: str
    phone_number: str

    boarding_bus: BusModelDTO
    destination_stop: BusStopModelDTO

    model_config = ConfigDict(from_attributes=True)


class BoardingRecordModelDTO(BaseModel):
    id: int
    user_id: int
    boarding_bus_id: int
    destination_stop_id: int
    verified: bool
    time_created: datetime

    model_config = ConfigDict(from_attributes=True)


class BoardingRecordInputDTO(BaseModel):
    user_otp: str


class BoardingRecordBypassInputDTO(BaseModel):
    user_id: int
