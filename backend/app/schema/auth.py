from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    org_code: str


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
