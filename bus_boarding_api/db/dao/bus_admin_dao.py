from typing import List

from fastapi import Depends
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from bus_boarding_api.db.dependencies import get_db_session
from bus_boarding_api.db.models.bus_admin import BusAdminModel
from bus_boarding_api.db.models.user import UserModel


class BusAdminDAO:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create(self, user_id: int, bus_id: int) -> None:
        self.session.add(
            BusAdminModel(user_id=user_id, bus_id=bus_id))

    async def get(self, user_id: int, bus_id: int) -> BusAdminModel | None:
        stmt = (
            select(BusAdminModel)
            .where(and_(
                BusAdminModel.user_id == user_id,
                BusAdminModel.bus_id == bus_id
            ))
        )
        result = await self.session.execute(stmt.limit(1))
        return result.scalar_one_or_none()

    async def get_all(self, bus_id) -> List[UserModel]:
        stmt = (
            select(UserModel)
            .join(BusAdminModel)
            .where(BusAdminModel.bus_id == bus_id)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().fetchall())

    async def delete(self, user_id: int, bus_id: int):
        bus_admin = await self.session.get(BusAdminModel, (user_id, bus_id))
        if bus_admin:
            await self.session.delete(bus_admin)
