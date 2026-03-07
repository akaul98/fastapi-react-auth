from pydantic import BaseModel, EmailStr

from app.schema.base import BaseSchema


class LoginRequest(BaseSchema):
    email: EmailStr
    org_code: str


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseSchema):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
