from pydantic import BaseModel, ConfigDict


class UserModelDTO(BaseModel):
    id: int
    student_id: str
    name: str

    model_config = ConfigDict(from_attributes=True)


class UserModelWithInfosDTO(BaseModel):
    id: int
    student_id: str
    name: str
    year: int
    boarding_bus_id: int
    destination_stop_id: int

    model_config = ConfigDict(from_attributes=True)


class UserModelInputDTO(BaseModel):
    student_id: str
    name: str
    phone_number: str
    year: int
    boarding_bus_id: int
    destination_stop_id: int


class AuthenticateInputDTO(BaseModel):
    student_id: str
    name: str
    phone_number: str


class TokenDTO(BaseModel):
    access_token: str
    token_type: str
