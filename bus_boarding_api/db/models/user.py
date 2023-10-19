from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func, expression
from sqlalchemy.sql.sqltypes import Integer, String, Boolean, DateTime

from bus_boarding_api.db.base import Base
from .boarding_info import BoardingInfoModel
from .boarding_record import BoardingRecordModel


class UserModel(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_id: Mapped[str] = mapped_column(String(length=10), nullable=False)
    name: Mapped[str] = mapped_column(String(length=100), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(length=20), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    role: Mapped[str] = mapped_column(String(length=20), nullable=False, server_default="USER")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=expression.true())

    boarding_info: Mapped["BoardingInfoModel"] = relationship(uselist=False, cascade="all, delete-orphan")
    boarding_records: Mapped[List["BoardingRecordModel"]] = relationship(cascade="all, delete-orphan")

    time_created: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    time_updated: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True, onupdate=func.now())
