from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func, expression
from sqlalchemy.sql.sqltypes import Integer, String, Boolean, DateTime

from bus_boarding_api.db.base import Base
from bus_boarding_api.db.models.boarding_record import BoardingRecordModel
# from bus_boarding_api.db.models.bus import BusModel
# from bus_boarding_api.db.models.bus_stop import BusStopModel


class UserModel(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_id: Mapped[str] = mapped_column(String(length=100), nullable=False)
    name: Mapped[str] = mapped_column(String(length=100), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(length=20), nullable=False)
    role: Mapped[str] = mapped_column(String(length=20), nullable=False, server_default="USER")
    totp_secret: Mapped[str] = mapped_column(String(length=100), nullable=True)
    totp_created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    boarding_bus_id: Mapped[int] = mapped_column(ForeignKey("bus.id"), nullable=True)
    destination_stop_id: Mapped[int] = mapped_column(ForeignKey("bus_stop.id"), nullable=True)

    boarding_bus: Mapped["BusModel"] = relationship()
    destination_stop: Mapped["BusStopModel"] = relationship()

    boarding_records: Mapped[List["BoardingRecordModel"]] = relationship()

    time_created: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    time_updated: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True, onupdate=func.now())
