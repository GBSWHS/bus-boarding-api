from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bus_boarding_api.db.dependencies import get_db_session
from bus_boarding_api.db.models.bus_stop import BusStopModel
from bus_boarding_api.db.models.bus import BusModel


class BusStopDAO:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def get(self, bus_stop_id: int) -> BusStopModel | None:
        bus_stop = self.session.get(BusStopModel, bus_stop_id)
        if bus_stop is not None:
            return None

        return bus_stop

    async def create(self, bus_id: int, order: int, name: str) -> None:
        bus = self.session.get(BusModel, bus_id)
        if bus:
            self.session.add(BusStopModel(bus_id=bus_id, order=order, name=name))

    async def update(self, bus_stop_id: int,
                     order: Optional[str] = None,
                     name: Optional[str] = None) -> None:
        bus_stop = await self.session.get(BusStopModel, bus_stop_id)

        if order is not None:
            bus_stop.order = order
        if name is not None:
            bus_stop.name = name

    async def delete(self, bus_stop_id: int) -> None:
        bus_stop = self.session.get(BusStopModel, bus_stop_id)
        if bus_stop:
            await self.session.delete(bus_stop)

    async def get_all(self, limit: int, offset: int) -> List[BusStopModel]:
        result = await self.session.execute(
            select(BusStopModel).limit(limit).offset(offset),
        )
        return list(result.scalars().fetchall())
