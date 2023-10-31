from pydantic import BaseModel, ConfigDict


class BusStopModelDTO(BaseModel):
    id: int
    name: str
    location: str

    model_config = ConfigDict(from_attributes=True)


class BusStopModelInputDTO(BaseModel):
    bus_id: int
    name: str
