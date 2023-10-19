from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bus_boarding_api.db.base import Base
# from bus_boarding_api.db.models.bus_stop import BusStopModel
from bus_boarding_api.db.models.bus_route import BusRouteModel
# from bus_boarding_api.db.models.boarding_record import BoardingRecordModel


class BusModel(Base):
    __tablename__ = "bus"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(length=10), nullable=False)
    destination: Mapped[int] = mapped_column(ForeignKey("bus_stop.id"))
    description: Mapped[str] = mapped_column(String(length=500), nullable=False, default="")

    bus_stops: Mapped[List["BusStopModel"]] = relationship(secondary="bus_route", back_populates="buses", viewonly=True)
    bus_stop_associations: Mapped[List["BusRouteModel"]] = relationship(back_populates="bus")

    boarding_records: Mapped[List["BoardingRecordModel"]] = relationship(viewonly=True, cascade="all, delete-orphan")

    time_created: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    time_updated: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True, onupdate=func.now())
