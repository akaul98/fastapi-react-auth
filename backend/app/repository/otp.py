from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.model.otp import OTP, OTPStatusEnum
from app.model.user import User
from app.model.organization import Organization
from datetime import datetime, timedelta
import secrets
import uuid


class OtpRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def validate_organization_and_user(self, user_id: str, organization_id: str):
        """Validate if organization exists and user belongs to that organization"""
        query = select(User).where(
            and_(
                User.id == user_id,
                User.organization_id == organization_id
            )
        )
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()
        return user is not None

    async def generate_and_store_otp(self, user_id: str, organization_id: str, phone_number: str):
        """Generate a 5-digit random OTP and store it in the database"""
        # Generate 5-digit random OTP
        otp_code = str(secrets.randbelow(90000) + 10000)  # Ensures 5 digits
        
        # Create OTP record
        otp_id = str(uuid.uuid4())
        otp_record = OTP()
        otp_record.id = otp_id
        otp_record.user_id = user_id
        otp_record.organization_id = organization_id
        otp_record.phone = phone_number
        otp_record.code = otp_code
        otp_record.status = OTPStatusEnum.PENDING
        otp_record.created_at = datetime.now()
        otp_record.expires_at = datetime.now() + timedelta(minutes=5)  # OTP expires in 5 minutes
        
        self.db.add(otp_record)
        await self.db.commit()
        await self.db.refresh(otp_record)
        
        return otp_record

    async def verify_otp(self, user_id: str, organization_id: str, phone_number: str, otp_code: str):
        """Verify the OTP and update its status to verified"""
        query = select(OTP).where(
            and_(
                OTP.user_id == user_id,
                OTP.organization_id == organization_id,
                OTP.phone == phone_number,
                OTP.code == otp_code,
                OTP.status == OTPStatusEnum.PENDING
            )
        ).order_by(OTP.created_at.desc())
        
        result = await self.db.execute(query)
        otp_record = result.scalar_one_or_none()
        
        if not otp_record:
            return None
        
        # Check if OTP has expired
        if datetime.now() > otp_record.expires_at:
            otp_record.status = OTPStatusEnum.EXPIRED
            await self.db.commit()
            return None
        
        # Mark OTP as verified
        otp_record.status = OTPStatusEnum.VERIFIED
        otp_record.verified_at = datetime.now()
        await self.db.commit()
        await self.db.refresh(otp_record)
        
        return otp_record

    async def get_otp_by_id(self, otp_id: str):
        """Get OTP record by ID"""
        query = select(OTP).where(OTP.id == otp_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()