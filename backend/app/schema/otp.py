from pydantic import BaseModel
from typing import Optional

from app.schema.base import BaseSchema


class OtpRequest(BaseSchema):
    user_id: str
    organization_id: str
    phone_number: str


class OtpVerifyRequest(BaseSchema):
    user_id: str
    organization_id: str
    otp_code: str
    phone_number: str


class OtpResponse(BaseSchema):
    message: str
    otp_id: Optional[str] = None