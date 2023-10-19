from pydantic import BaseModel, ConfigDict


class BusStopModelDTO(BaseModel):
    id: int
    bus_id: int
    order: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class BusStopModelInputDTO(BaseModel):
    bus_id: int
    order: int
    name: str
