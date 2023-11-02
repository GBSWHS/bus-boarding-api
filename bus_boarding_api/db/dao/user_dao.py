from datetime import datetime
from typing import List

from fastapi import Depends
from sqlalchemy import select, insert, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from bus_boarding_api.db.dependencies import get_db_session
from bus_boarding_api.db.models.bus import BusModel
from bus_boarding_api.db.models.user import UserModel


class UserDAO:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_super_user(self) -> None:
        self.session.add(UserModel(student_id='_', name='_', phone_number='_', role='ADMINISTRATOR'))

    async def create_users(self, users: List[UserModel]) -> None:
        bus_ids = set(user.boarding_bus_id for user in users)
        for bus_id in bus_ids:
            bus = await self.session.get(BusModel, bus_id)
            if not bus:
                raise Exception(f'Bus {bus_id} does not exist.')

        user_list = [
            {
                'student_id': user.student_id,
                'name': user.name,
                'phone_number': user.phone_number,
                'boarding_bus_id': user.boarding_bus_id,
                'destination_stop_id': user.destination_stop_id,
                'role': 'USER',
            }
            for user in users
        ]

        await self.session.execute(insert(UserModel), user_list)

    async def create(self, student_id: str, name: str, phone_number: str, bus_id: int, stop_id: int) -> None:
        user = UserModel(
            student_id=student_id,
            name=name,
            phone_number=phone_number,
        )
        self.session.add(user)

    async def update_totp_secret(self, user_id: int, totp_secret: str) -> None:
        user = await self.session.get(UserModel, user_id)
        if user:
            user.totp_secret = totp_secret
            user.totp_created_at = datetime.now()

    async def delete(self, user_id: int) -> None:
        user = self.session.get(UserModel, user_id)
        if user:
            await self.session.delete(user)

    async def get(self, user_id: int) -> UserModel:
        stmt = (
            select(UserModel)
            .where(UserModel.id == user_id)
        )
        stmt = stmt.options(joinedload(UserModel.boarding_bus))
        stmt = stmt.options(joinedload(UserModel.destination_stop))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_password(self, password: str) -> UserModel:
        stmt = (
            select(UserModel)
            .where(and_(
                UserModel.student_id == password,
                UserModel.role == 'ADMINISTRATOR'
            ))
        )
        result = await self.session.execute(stmt.limit(1))
        return result.scalar_one_or_none()

    async def get_by_infos(self, student_id: str, name: str, phone_number: str) -> UserModel:
        stmt = (
            select(UserModel)
            .where(and_(
                UserModel.student_id == student_id,
                UserModel.name == name,
                UserModel.phone_number == phone_number,
                UserModel.role != 'ADMINISTRATOR'
            ))
        )
        result = await self.session.execute(stmt.limit(1))
        return result.scalar_one_or_none()

    async def get_all(self, limit: int, offset: int) -> List[UserModel]:
        stmt = select(UserModel)
        stmt = stmt.options(joinedload(UserModel.boarding_bus))
        stmt = stmt.options(joinedload(UserModel.destination_stop))

        result = await self.session.execute(stmt.limit(limit).offset(offset))
        return list(result.scalars().fetchall())

    async def get_all_by_bus_id(self, bus_id: int, limit: int, offset: int) -> List[UserModel]:
        stmt = (
            select(UserModel)
            .where(and_(
                UserModel.boarding_bus_id == bus_id,
                UserModel.role != 'ADMINISTRATOR',
            ))
        )
        stmt = stmt.options(joinedload(UserModel.boarding_bus))
        stmt = stmt.options(joinedload(UserModel.destination_stop))
        result = await self.session.execute(stmt.limit(limit).offset(offset))
        return list(result.scalars().fetchall())

    async def filter_by_name(self, name: str, limit: int, offset: int) -> List[UserModel]:
        stmt = (
            select(UserModel)
            .where(UserModel.name.like(name))
        )
        result = await self.session.execute(stmt.limit(limit).offset(offset))
        return list(result.scalars().fetchall())
