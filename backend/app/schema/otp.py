from typing import Optional
from pydantic import EmailStr
from app.schema.base import BaseSchema


class OtpRequest(BaseSchema):
    user_id: str
    organization_id: str
    email: EmailStr


class OtpVerifyRequest(BaseSchema):
    user_id: str
    organization_id: str
    otp_code: str
    email: EmailStr
    otp_id: str
    


class OtpResponse(BaseSchema):
    message: str
    otp_id: Optional[str] = None
    email:EmailStr
    organization_id: str
    user_id: str
    otp_code: Optional[str] = None