import secrets
import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.model.otp import OTP, OTPStatusEnum
from app.model.user import User


class OtpRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def validate_organization_and_user(self, user_id: str, organization_id: str) -> bool:
        result = await self.db.execute(
            select(User).where(
                and_(User.id == user_id, User.organization_id == organization_id)
            )
        )
        return result.scalar_one_or_none() is not None

    async def generate_and_store_otp(
        self, user_id: str, organization_id: str, phone_number: str
    ) -> OTP:
        # Expire any existing pending OTPs for this user before creating a new one
        pending = await self.db.execute(
            select(OTP).where(
                and_(
                    OTP.user_id == user_id,
                    OTP.organization_id == organization_id,
                    OTP.status == OTPStatusEnum.PENDING,
                )
            )
        )
        for old_otp in pending.scalars().all():
            old_otp.status = OTPStatusEnum.EXPIRED

        now = datetime.now(timezone.utc).replace(tzinfo=None)
        otp_code = str(secrets.randbelow(90000) + 10000)

        otp_record = OTP()
        otp_record.id = str(uuid.uuid4())
        otp_record.user_id = user_id
        otp_record.organization_id = organization_id
        otp_record.phone = phone_number
        otp_record.code = otp_code
        otp_record.status = OTPStatusEnum.PENDING
        otp_record.created_at = now
        otp_record.expires_at = now + timedelta(minutes=5)

        self.db.add(otp_record)
        await self.db.commit()
        await self.db.refresh(otp_record)
        return otp_record

    async def verify_otp(
        self, user_id: str, organization_id: str, phone_number: str, otp_code: str
    ) -> OTP | None:
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        result = await self.db.execute(
            select(OTP)
            .where(
                and_(
                    OTP.user_id == user_id,
                    OTP.organization_id == organization_id,
                    OTP.phone == phone_number,
                    OTP.code == otp_code,
                    OTP.status == OTPStatusEnum.PENDING,
                    OTP.expires_at > now,
                )
            )
            .order_by(OTP.created_at.desc())
        )
        otp_record = result.scalar_one_or_none()
        if not otp_record:
            return None

        otp_record.status = OTPStatusEnum.VERIFIED
        otp_record.verified_at = datetime.now(timezone.utc).replace(tzinfo=None)
        await self.db.commit()
        await self.db.refresh(otp_record)
        return otp_record

    async def get_otp_by_id(self, otp_id: str) -> OTP | None:
        result = await self.db.execute(select(OTP).where(OTP.id == otp_id))
        return result.scalar_one_or_none()
