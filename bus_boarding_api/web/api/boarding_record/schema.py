from pydantic import BaseModel, ConfigDict


class BoardingRecordModelDTO(BaseModel):
    id: int
    user_id: int
    boarding_bus_id: int
    destination_stop_id: int

    model_config = ConfigDict(from_attributes=True)
