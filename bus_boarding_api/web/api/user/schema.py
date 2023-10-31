from typing import Optional

from pydantic import BaseModel, ConfigDict

from bus_boarding_api.web.api.bus.schema import BusModelDTO
from bus_boarding_api.web.api.bus_stop.schema import BusStopModelDTO


class UserModelDTO(BaseModel):
    id: int
    student_id: str
    name: str
    phone_number: str
    role: str
    boarding_bus: Optional[BusModelDTO]
    destination_stop: Optional[BusStopModelDTO]

    model_config = ConfigDict(from_attributes=True)


class UserModelWithInfosDTO(BaseModel):
    id: int
    student_id: str
    name: str
    phone_number: str
    boarding_bus_id: int
    destination_stop_id: int

    model_config = ConfigDict(from_attributes=True)


class UserModelInputDTO(BaseModel):
    student_id: str
    name: str
    phone_number: str
    boarding_bus_id: int
    destination_stop_id: int


class AuthenticateInputDTO(BaseModel):
    student_id: str | None
    name: str | None
    phone_number: str | None
    password: str | None


class TokenDTO(BaseModel):
    access_token: str
    totp_secret: str
    type: str
