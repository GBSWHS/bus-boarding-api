from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import DateTime

from bus_boarding_api.db.base import Base


class BoardingRecordModel(Base):
    __tablename__ = "boarding_record"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    destination_stop_id: Mapped[int] = mapped_column(ForeignKey("bus_stop.id"))
    boarding_bus_id: Mapped[int] = mapped_column(ForeignKey("bus.id"))
    verified: Mapped[bool] = mapped_column(nullable=False, default=False)

    user: Mapped["UserModel"] = relationship(viewonly=True, single_parent=True, cascade="all, delete-orphan")
    destination_stop: Mapped["BusStopModel"] = relationship(single_parent=True, cascade="all, delete-orphan")
    boarding_bus: Mapped["BusModel"] = relationship(single_parent=True, cascade="all, delete-orphan")

    time_created: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
