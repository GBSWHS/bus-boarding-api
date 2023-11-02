from datetime import datetime
from typing import List

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from bus_boarding_api.db.dependencies import get_db_session
from bus_boarding_api.db.models.boarding_record import BoardingRecordModel
from bus_boarding_api.db.models.user import UserModel
from bus_boarding_api.db.models.bus import BusModel
from bus_boarding_api.db.models.bus_stop import BusStopModel


class BoardingRecordDAO:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create(self, user_id: int, bus_id: int, destination_stop_id: int) -> None:
        user_result = await self.session.execute(select(UserModel.id).where(UserModel.id == user_id))
        if not user_result.scalar_one_or_none():
            raise ValueError(f"User with ID {user_id} does not exist.")

        bus_result = await self.session.execute(select(BusModel.id).where(BusModel.id == bus_id))
        if not bus_result.scalar_one_or_none():
            raise ValueError(f"Bus with ID {bus_id} does not exist.")

        stop_result = await self.session.execute(select(BusStopModel.id).where(BusStopModel.id == destination_stop_id))
        if not stop_result.scalar_one_or_none():
            raise ValueError(f"Stop with ID {destination_stop_id} does not exist.")

        self.session.add(BoardingRecordModel(user_id=user_id,
                                             boarding_bus_id=bus_id,
                                             destination_stop_id=destination_stop_id))

    async def get_today_record_by_bus_id(self, bus_id: int) -> List[BoardingRecordModel]:
        stmt = (
            select(BoardingRecordModel)
            .where(BoardingRecordModel.boarding_bus_id == bus_id)
            .where(BoardingRecordModel.time_created >= datetime.now().date())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_all(self):
        stmt = select(BoardingRecordModel)
        stmt = stmt.options(joinedload(BoardingRecordModel.user))
        stmt = stmt.options(joinedload(BoardingRecordModel.destination_stop))
        stmt = stmt.options(joinedload(BoardingRecordModel.boarding_bus))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_user(self, user_id: int):
        stmt = (
            select(BoardingRecordModel)
            .where(BoardingRecordModel.user_id == user_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete(self, boarding_record_id: int) -> None:
        boarding_record = self.session.get(BoardingRecordModel, boarding_record_id)
        if boarding_record:
            await self.session.delete(boarding_record)
