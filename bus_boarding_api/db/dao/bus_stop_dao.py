from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bus_boarding_api.db.dependencies import get_db_session
from bus_boarding_api.db.models.bus_stop import BusStopModel


class BusStopDAO:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create(self, order: int, name: str) -> None:
        self.session.add(BusStopModel(order=order, name=name))

    async def update(self, bus_stop_id: int,
                     order: Optional[str] = None,
                     name: Optional[str] = None) -> None:
        bus_stop = await self.session.get(BusStopModel, bus_stop_id)

        if order is not None:
            bus_stop.order = order
        if name is not None:
            bus_stop.name = name

    async def delete(self, bus_id: int) -> None:
        bus_stop = self.session.get(BusStopModel, bus_id)
        if bus_stop:
            await self.session.delete(bus_stop)

    async def get_all(self, limit=50) -> List[BusStopModel]:
        result = await self.session.execute(
            select(BusStopModel).limit(limit),
        )
        return list(result.scalars().fetchall())

    async def filter_by_name(self, name: Optional[str] = None, limit=50) -> List[BusStopModel]:
        query = select(BusStopModel)
        if name:
            query = query.where(BusStopModel.name.like(name))
        result = await self.session.execute(query)
        return list(result.scalars().fetchall())
