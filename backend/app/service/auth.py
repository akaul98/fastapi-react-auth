import uuid
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.repository.auth import AuthRepository
from app.repository.otp import OtpRepository
from app.repository.revoked_token import RevokedTokenRepository
from app.schema.auth import LoginRequest
from app.schema.otp import OtpVerifyRequest


def _create_token(payload: dict, expires_delta: timedelta) -> str:
    payload = {
        **payload,
        "jti": str(uuid.uuid4()),
        "exp": datetime.now(timezone.utc) + expires_delta,
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


class AuthService:
    def __init__(self, db: AsyncSession):
        self.repo = AuthRepository(db)
        self.otp_repo = OtpRepository(db)
        self.revoked_repo = RevokedTokenRepository(db)

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

        return {"message": "OTP sent successfully", "otp_id": otp_record.id}

    async def verify_and_generate_tokens(self, otp_verify: OtpVerifyRequest) -> dict:
        otp_record = await self.otp_repo.verify_otp(
            otp_verify.user_id,
            otp_verify.organization_id,
            otp_verify.phone_number,
            otp_verify.otp_code,
        )
        if not otp_record:
            raise ValueError("Invalid or expired OTP")

        result = await self.repo.get_user_and_org_by_verified_otp(otp_record.id)
        if not result:
            raise ValueError("User or organization not found")

        user, org = result
        claims = {
            "sub": user.id,
            "theme": user.theme.value,
            "org_id": org.id,
            "org_code": org.org_code,
        }

        access_token = _create_token(
            {**claims, "type": "access"},
            timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        refresh_token = _create_token(
            {**claims, "type": "refresh"},
            timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        )
        return {"access_token": access_token, "refresh_token": refresh_token}

    async def refresh_token(self, refresh_token: str) -> dict:
        try:
            payload = jwt.decode(
                refresh_token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
        except JWTError:
            raise ValueError("Invalid or expired refresh token")

        if payload.get("type") != "refresh":
            raise ValueError("Invalid token type")

        jti = payload.get("jti")
        if jti and await self.revoked_repo.is_revoked(jti):
            raise ValueError("Refresh token has been revoked")

        # Revoke the used refresh token so it cannot be reused
        if jti:
            exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
            await self.revoked_repo.revoke(jti, exp)

        claims = {
            "sub": payload["sub"],
            "theme": payload["theme"],
            "org_id": payload["org_id"],
            "org_code": payload["org_code"],
        }
        access_token = _create_token(
            {**claims, "type": "access"},
            timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        new_refresh_token = _create_token(
            {**claims, "type": "refresh"},
            timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        )
        return {"access_token": access_token, "refresh_token": new_refresh_token}
