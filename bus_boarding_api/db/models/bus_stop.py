from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import Integer, String, DateTime

from bus_boarding_api.db.base import Base


class BusStopModel(Base):
    __tablename__ = "bus_stop"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    bus_id: Mapped[int] = mapped_column(ForeignKey("bus.id"))
    order: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(length=255), nullable=False)

    time_created: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    time_updated: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True, onupdate=func.now())
