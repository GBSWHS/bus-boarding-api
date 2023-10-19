from typing import List

from fastapi import Depends
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from bus_boarding_api.db.dependencies import get_db_session
from bus_boarding_api.db.models.user import UserModel


class UserDAO:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_super_user(self) -> None:
        self.session.add(UserModel(student_id='_', name='_', phone_number='_', year=2000, role='ADMINISTRATOR'))

    async def create(self, student_id: str, name: str, phone_number: str, year: int, bus_id: int, stop_id: int) -> None:
        user = UserModel(
            student_id=student_id,
            name=name,
            phone_number=phone_number,
            year=year,
        )
        self.session.add(user)

    # async def update_student_id(self, user_id: int,
    #                  student_id: Optional[str] = None,
    #                  name: Optional[str] = None,
    #                  phone_number: Optional[str] = None) -> None:
    #     user = await self.session.get(UserModel, user_id)
    #
    #     if student_id:
    #         user.student_id = student_id
    #     if name:
    #         user.name = name
    #     if phone_number:
    #         user.phone_number = phone_number
    #
    # async def update_name(self, user_id: int,
    #                  student_id: Optional[str] = None,
    #                  name: Optional[str] = None,
    #                  phone_number: Optional[str] = None) -> None:
    #     user = await self.session.get(UserModel, user_id)
    #
    #     if student_id:
    #         user.student_id = student_id
    #     if name:
    #         user.name = name
    #     if phone_number:
    #         user.phone_number = phone_number

    async def delete(self, user_id: int) -> None:
        user = self.session.get(UserModel, user_id)
        if user:
            await self.session.delete(user)

    async def get(self, user_id: int) -> UserModel:
        stmt = (
            select(UserModel)
            .where(UserModel.id == user_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_infos(self, student_id: str, name: str, phone_number: str) -> UserModel:
        stmt = (
            select(UserModel)
            .where(and_(
                UserModel.student_id == student_id,
                UserModel.name == name,
                UserModel.phone_number == phone_number
            ))
        )
        result = await self.session.execute(stmt.limit(1))
        return result.scalar_one_or_none()

    async def get_all(self, year: int, limit: int, offset: int) -> List[UserModel]:
        stmt = select(UserModel)
        if year:
            stmt = stmt.where(UserModel.year == year)
        result = await self.session.execute(stmt.limit(limit).offset(offset))
        return list(result.scalars().fetchall())

    async def filter_by_name(self, name: str, limit: int, offset: int) -> List[UserModel]:
        stmt = (
            select(UserModel)
            .where(UserModel.name.like(name))
        )
        result = await self.session.execute(stmt.limit(limit).offset(offset))
        return list(result.scalars().fetchall())
