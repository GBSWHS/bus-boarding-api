from datetime import datetime
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from bus_boarding_api.db.models.boarding_record import BoardingRecordModel
from bus_boarding_api.db.models.bus import BusModel


class BusDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, name: str, destination: int, description: str) -> None:
        # TODO destination check

        bus = BusModel(name=name, destination=destination, description=description)
        self.session.add(bus)

    async def update(self, bus_id: int,
                     name: Optional[str] = None,
                     destination: Optional[str] = None,
                     description: Optional[str] = None) -> None:
        bus = await self.session.get(BusModel, bus_id)

        if name is not None:
            bus.name = name
        if destination is not None:
            bus.destination = destination
        if description is not None:
            bus.description = description

        # query = (
        #     update(BusModel)
        #     .where(BusModel.id == bus_id)
        #     .values()
        # )

    async def delete(self, bus_id: int) -> None:
        bus = self.session.get(BusModel, bus_id)
        if bus:
            await self.session.delete(bus)

    async def get_all(self, limit: int, offset: int) -> List[BusModel]:
        query = select(BusModel).limit(limit).offset(offset)
        result = await self.session.execute(query)
        return list(result.scalars().fetchall())

    async def get(self,
                  bus_id: int,
                  load_stops: bool = False,
                  load_boarding_records: bool = False) -> BusModel:
        stmt = select(BusModel).where(BusModel.id == bus_id)

        if load_stops:
            stmt = stmt.options(selectinload(BusModel.bus_stops))

        if load_boarding_records:
            stmt = stmt.options(selectinload(BusModel.boarding_records)).filter(BoardingRecordModel.time_created > datetime.now().replace(hour=0, minute=0, second=0, microsecond=0))

        result = await self.session.execute(stmt.limit(1))
        return result.scalar_one_or_none()

    async def filter_by_destination(self, destination: Optional[str] = None) -> List[BusModel]:
        query = select(BusModel)
        if destination:
            query = query.where(BusModel.destination.like(destination))
        result = await self.session.execute(query)
        return list(result.scalars().fetchall())
