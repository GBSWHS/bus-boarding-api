from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import DateTime

from bus_boarding_api.db.base import Base
from .bus import BusModel
from .user import UserModel


class BusAdminModel(Base):
    __tablename__ = "bus_admin"
    bus_id: Mapped[int] = mapped_column(ForeignKey('bus.id'), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key=True)

    bus: Mapped[List["BusModel"]] = relationship()
    user: Mapped[List["UserModel"]] = relationship()

    time_created: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    time_updated: Mapped[DateTime] = mapped_column(DateTime(timezone=True), onupdate=func.now())
