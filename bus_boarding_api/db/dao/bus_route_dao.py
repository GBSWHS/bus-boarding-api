from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from bus_boarding_api.db.dependencies import get_db_session
from bus_boarding_api.db.models.bus_route import BusRouteModel


class BusRouteDAO:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create(self, name: str, bus_id: str, stop_id: str) -> None:
        bus_route = BusRouteModel(name=name, bus_id=bus_id, stop_id=stop_id)
        self.session.add(bus_route)

    async def delete(self, bus_route_id: int) -> None:
        bus_route = self.session.get(BusRouteModel, bus_route_id)
        if bus_route:
            await self.session.delete(bus_route)
