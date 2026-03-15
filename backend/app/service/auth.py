from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from app.repository.auth import AuthRepository
from app.repository.otp import OtpRepository
from app.schema.auth import LoginRequest
from app.schema.otp import OtpVerifyRequest
import os
from app.repository.organization import OrganizationRepository

SECRET_KEY = os.environ["JWT_SECRET_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7


def _create_token(payload: dict, expires_delta: timedelta) -> str:
    payload["exp"] = datetime.now(timezone.utc) + expires_delta
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


class AuthService:
    def __init__(self, db: AsyncSession):
        self.repo = AuthRepository(db,OrganizationRepository(db))
        self.otp_repo = OtpRepository(db)

    async def login(self, login_data: LoginRequest) -> dict:
        user = await self.repo.get_user_by_email_and_org_code(
            login_data.email, login_data.org_code
        )

        if not user:
            raise ValueError("Invalid email or organization code")

        otp_record = await self.otp_repo.generate_and_store_otp(
            user.id, user.organization_id, user.phone
        )

        # TODO: send SMS via Twilio or similar
        # await send_sms(user.phone, f"Your OTP is: {otp_record.code}")

        return {
            "message": "OTP sent successfully",
            "otp_id": otp_record.id
        }

    async def verify_and_generate_tokens(self, otp_verify: OtpVerifyRequest) -> dict:
  
        result = await self.repo.get_user_and_org_by_verified_otp(otp_verify.otp_id)
        if not result:
            raise ValueError("Invalid or expired OTP")
        user, org = result

        claims = {
            "sub": user.id,
            "theme": user.theme.value,
            "org_id": org.id,
            "org_code": org.org_code,
        }

        access_token = _create_token(
            {**claims, "type": "access"},
            timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        refresh_token = _create_token(
            {**claims, "type": "refresh"},
            timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    async def refresh_token(self, refresh_token: str) -> dict:
        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise ValueError("Invalid or expired refresh token")

        if payload.get("type") != "refresh":
            raise ValueError("Invalid token type")

        claims = {
            "sub": payload["sub"],
            "theme": payload["theme"],
            "org_id": payload["org_id"],
            "org_code": payload["org_code"],
        }

        access_token = _create_token(
            {**claims, "type": "access"},
            timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        new_refresh_token = _create_token(
            {**claims, "type": "refresh"},
            timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        )

        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token
        }
