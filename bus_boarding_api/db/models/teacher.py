from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import String, DateTime

from bus_boarding_api.db.base import Base


class TeacherModel(Base):
    __tablename__ = "teacher"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(length=100), nullable=False)
    password: Mapped[str] = mapped_column(String(length=255), nullable=False)

    time_created: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    time_updated: Mapped[DateTime] = mapped_column(DateTime(timezone=True), onupdate=func.now())

