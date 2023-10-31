import base64
from datetime import datetime

import pyotp
from fastapi import APIRouter, HTTPException
from fastapi.param_functions import Depends

from bus_boarding_api.authentication import PermissionChecker, get_current_user
from bus_boarding_api.db.dao.boarding_record_dao import BoardingRecordDAO
from bus_boarding_api.db.dao.bus_admin_dao import BusAdminDAO
from bus_boarding_api.db.dao.user_dao import UserDAO
from bus_boarding_api.db.models.user import UserModel
from bus_boarding_api.permissions.models_permissions import (BusStop, BoardingRecord,
                                                             User, Bus)
from bus_boarding_api.web.api.boarding_record.schema import BoardingRecordInputDTO

router = APIRouter()


@router.get("/", dependencies=[Depends(PermissionChecker([User.permissions.READ, Bus.permissions.READ, BusStop.permissions.READ, BoardingRecord.permissions.READ]))])
async def get_all_boarding_records(
    boarding_record_dao: BoardingRecordDAO = Depends(),
):
    return await boarding_record_dao.get_all()


@router.post("/", dependencies=[Depends(PermissionChecker([
    BoardingRecord.permissions.CREATE,
]))])
async def create_boarding_record(
    new_boarding_record: BoardingRecordInputDTO,
    user_dao: UserDAO = Depends(),
    bus_admin_dao: BusAdminDAO = Depends(),
    boarding_record_dao: BoardingRecordDAO = Depends(),
    current_user: UserModel = Depends(get_current_user),
):
    decoded_user_otp = base64.b64decode(new_boarding_record.user_otp).decode('ascii')
    otp, user_id = decoded_user_otp.split(';')
    if otp is None or user_id is None:
        raise HTTPException(status_code=400, detail="지원하지 않는 QR코드 형식입니다.")

    user = await user_dao.get(int(user_id))
    if user is None:
        raise HTTPException(status_code=404, detail="존재하지 않는 사용자 입니다.")

    if (datetime.utcnow() - user.totp_created_at).total_seconds() > 86400:
        raise HTTPException(status_code=400, detail="유효하지 않은 OTP 입니다.")

    if not pyotp.TOTP(user.totp_secret).verify(otp):
        raise HTTPException(status_code=400, detail="유효하지 않은 OTP 입니다.")

    bus_admin = await bus_admin_dao.get(current_user.id, user.boarding_bus_id)
    if bus_admin is None:
        raise HTTPException(status_code=404, detail="해당 버스 탑승자가 아닙니다.")

    await boarding_record_dao.create(
        user_id=user.id,
        bus_id=user.boarding_bus_id,
        destination_stop_id=user.destination_stop_id,
    )
