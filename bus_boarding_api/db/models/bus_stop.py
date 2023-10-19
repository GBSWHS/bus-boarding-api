from typing import List

from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bus_boarding_api.db.base import Base
from bus_boarding_api.db.models.bus_route import BusRouteModel


class BusStopModel(Base):
    __tablename__ = "bus_stop"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(length=255), nullable=False)
    location: Mapped[str] = mapped_column(String(length=512), nullable=False)

    buses: Mapped[List["BusModel"]] = relationship(secondary="bus_route", back_populates="bus_stops", viewonly=True)
    bus_associations: Mapped[List["BusRouteModel"]] = relationship(back_populates="bus_stop")

    time_created: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    time_updated: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True, onupdate=func.now())
