from pydantic import BaseModel
from typing import Optional


class OtpRequest(BaseModel):
    user_id: str
    organization_id: str
    phone_number: str


class OtpVerifyRequest(BaseModel):
    user_id: str
    organization_id: str
    otp_code: str
    phone_number: str


class OtpResponse(BaseModel):
    message: str
    otp_id: Optional[str] = None