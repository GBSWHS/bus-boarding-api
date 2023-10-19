from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bus_boarding_api.db.base import Base
from bus_boarding_api.db.models.bus import BusModel
from bus_boarding_api.db.models.user import UserModel


class BusAdminModel(Base):
    __tablename__ = "bus_admin"
    bus_id: Mapped[int] = mapped_column(ForeignKey('bus.id'), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key=True)

    bus: Mapped[List["BusModel"]] = relationship(single_parent=True, cascade="all, delete-orphan")
    user: Mapped[List["UserModel"]] = relationship(single_parent=True, cascade="all, delete-orphan")

    time_created: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    time_updated: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True, onupdate=func.now())
