from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import DateTime

from bus_boarding_api.db.base import Base


class BoardingInfoModel(Base):
    __tablename__ = "boarding_info"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), unique=True)
    boarding_bus_id: Mapped[int] = mapped_column(ForeignKey("bus.id"))
    destination_stop_id: Mapped[int] = mapped_column(ForeignKey("bus_stop.id"))

    time_created: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    time_updated: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True, onupdate=func.now())
