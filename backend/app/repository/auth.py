from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.model.user import User
from app.model.organization import Organization
from app.model.otp import OTP, OTPStatusEnum


class AuthRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email_and_org_code(self, email: str, org_code: str) -> User | None:
        result = await self.db.execute(
            select(User)
            .join(Organization, User.organization_id == Organization.id)
            .where(
                (User.email == email) &
                (Organization.org_code == org_code) &
                (User.status == True) &
                (Organization.status == True)
            )
        )
        return result.scalars().first()

    async def get_user_and_org_by_verified_otp(self, otp_id: str) -> tuple[User, Organization] | None:
        result = await self.db.execute(
            select(User, Organization)
            .join(Organization, User.organization_id == Organization.id)
            .join(OTP, OTP.user_id == User.id)
            .where(
                (OTP.id == otp_id) &
                (OTP.status == OTPStatusEnum.VERIFIED)
            )
        )
        row = result.first()
        if not row:
            return None
        return row[0], row[1]
