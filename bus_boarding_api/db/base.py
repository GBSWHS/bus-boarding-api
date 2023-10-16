from sqlalchemy.orm import DeclarativeBase

from bus_boarding_api.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
