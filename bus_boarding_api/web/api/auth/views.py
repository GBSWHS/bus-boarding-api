import pyotp
from fastapi import APIRouter, HTTPException, Form
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from bus_boarding_api.authentication import (authenticate_user, authenticate_admin,
                                             create_access_token)
from bus_boarding_api.db.dao.user_dao import UserDAO
from bus_boarding_api.db.dependencies import get_db_session
from bus_boarding_api.web.api.auth.schema import (TokenDTO, UserAuthInputDTO,
                                                  AdminAuthInputDTO)

router = APIRouter()


async def generate_token_and_response(user, user_dao):
    base32_string = pyotp.random_base32()
    access_token = create_access_token(data=user.id)
    await user_dao.update_totp_secret(user_id=user.id, totp_secret=base32_string)

    return {
        "access_token": access_token,
        "totp_secret": base32_string,
        "type": user.role,
    }


@router.post("/user", response_model=TokenDTO)
async def login_user(form_data: UserAuthInputDTO, db: AsyncSession = Depends(get_db_session)):
    user_dao = UserDAO(db)

    user = await authenticate_user(
        student_id=form_data.student_id,
        name=form_data.name,
        phone_number=form_data.phone_number,
        user_dao=user_dao
    )

    if not user:
        raise HTTPException(status_code=401, detail="일치하지 않는 정보입니다")

    return await generate_token_and_response(user, user_dao)


@router.post("/admin", response_model=TokenDTO)
async def login_admin(form_data: AdminAuthInputDTO, db: AsyncSession = Depends(get_db_session)):
    user_dao = UserDAO(db)

    user = await authenticate_admin(student_id=form_data.password, user_dao=user_dao)

    if not user:
        raise HTTPException(status_code=401, detail="일치하지 않는 정보입니다")

    return await generate_token_and_response(user, user_dao)


@router.post("/swagger", response_model=TokenDTO)
async def login_swagger(password: str = Form(...), db: AsyncSession = Depends(get_db_session)):
    user_dao = UserDAO(db)

    user = await authenticate_admin(student_id=password, user_dao=user_dao)

    if not user:
        raise HTTPException(status_code=401, detail="일치하지 않는 정보입니다")

    return await generate_token_and_response(user, user_dao)
