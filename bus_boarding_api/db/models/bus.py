from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import String, DateTime

from bus_boarding_api.db.base import Base
from .bus_stop import BusStopModel
from .boarding_info import BoardingInfoModel
from .boarding_record import BoardingRecordModel


class BusModel(Base):
    __tablename__ = "bus"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(length=10), nullable=False)
    destination: Mapped[str] = mapped_column(String(length=255), nullable=False, default="")
    description: Mapped[str] = mapped_column(String(length=500), nullable=False, default="")

    stops: Mapped[List["BusStopModel"]] = relationship()
    boarding_infos: Mapped[List["BoardingInfoModel"]] = relationship()
    boarding_records: Mapped[List["BoardingRecordModel"]] = relationship()

    time_created: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    time_updated: Mapped[DateTime] = mapped_column(DateTime(timezone=True), onupdate=func.now())
