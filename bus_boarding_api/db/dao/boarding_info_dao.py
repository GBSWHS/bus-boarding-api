from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bus_boarding_api.db.dependencies import get_db_session
from bus_boarding_api.db.models.boarding_info import BoardingInfoModel
from bus_boarding_api.db.models.user import UserModel
from bus_boarding_api.db.models.bus import BusModel
from bus_boarding_api.db.models.bus_stop import BusStopModel


class BoardingInfoDAO:
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

        self.session.add(BoardingInfoModel(user_id=user_id,
                                           boarding_bus_id=bus_id,
                                           destination_stop_id=destination_stop_id))

    async def get_by_user(self, user_id: int):
        stmt = (
            select(BoardingInfoModel)
            .where(BoardingInfoModel.user_id == user_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete(self, boarding_info_id: int) -> None:
        boarding_info = self.session.get(BoardingInfoModel, boarding_info_id)
        if boarding_info:
            await self.session.delete(boarding_info)
