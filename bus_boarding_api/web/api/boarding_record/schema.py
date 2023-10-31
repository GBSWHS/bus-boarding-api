from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BoardingRecordModelDTO(BaseModel):
    id: int
    user_id: int
    boarding_bus_id: int
    destination_stop_id: int
    time_created: datetime

    model_config = ConfigDict(from_attributes=True)


class BoardingRecordInputDTO(BaseModel):
    user_otp: str
