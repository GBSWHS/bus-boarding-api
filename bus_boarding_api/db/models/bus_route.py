from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bus_boarding_api.db.base import Base
# from bus_boarding_api.db.models.bus_stop import BusStopModel
# from bus_boarding_api.db.models.bus import BusModel


class BusRouteModel(Base):
    __tablename__ = 'bus_route'

    bus_id: Mapped[int] = mapped_column(ForeignKey('bus.id'), primary_key=True)
    bus_stop_id: Mapped[int] = mapped_column(ForeignKey('bus_stop.id'), primary_key=True)

    bus: Mapped["BusModel"] = relationship(back_populates="bus_stop_associations")
    bus_stop: Mapped["BusStopModel"] = relationship(back_populates="bus_associations")
