from pydantic import BaseModel


class UserAuthInputDTO(BaseModel):
    student_id: str
    name: str
    phone_number: str


class AdminAuthInputDTO(BaseModel):
    password: str


class TokenDTO(BaseModel):
    access_token: str
    totp_secret: str
    type: str
