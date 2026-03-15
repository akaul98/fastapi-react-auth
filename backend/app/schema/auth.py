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


class CurrentUser(BaseModel):
    user_id: str
    org_id: str
    org_code: str
    theme: str
