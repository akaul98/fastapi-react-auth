from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.model.user import User
from app.model.organization import Organization
from app.model.otp import OTP, OTPStatusEnum
from app.repository.organization import OrganizationRepository
from app.service import organization


class AuthRepository:
    def __init__(self, db: AsyncSession,org_service: OrganizationRepository):
        self.db = db
        self.org_service = org_service

    async def get_user_by_email_and_org_code(self, email: str, org_code: str) -> User | None:
        orgData=await self.org_service.get_org_by_code(org_code)
        if not orgData:
            return None
        
        result = await self.db.execute(
            select(User)
            .where(
                (User.email == email)  &
                (User.status == True) &
                (User.organization_id == orgData.id) &
                (orgData.status == True)
            )
        )
        
        resp= result.scalars().first()
        return resp
    


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

        await self.db.execute(
            update(OTP).where(OTP.id == otp_id).values(status=OTPStatusEnum.EXPIRED)
        )
        await self.db.commit()

        return row[0], row[1]
