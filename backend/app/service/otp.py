from app.schema.otp import OtpRequest, OtpVerifyRequest, OtpResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.repository.otp import OtpRepository


class OtpService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = OtpRepository(db)

    async def send_otp(self, otp_request: OtpRequest):
        """
        Send OTP by:
        1. Validating organization and user
        2. Generating 5-digit random OTP
        3. Storing in database
        """
        # Step 1: Validate if organization exists and user belongs to it
        is_valid = await self.repo.validate_organization_and_user(
            otp_request.user_id,
            otp_request.organization_id
        )
        
        if not is_valid:
            raise ValueError("Invalid user or organization")
        
        # Step 2 & 3: Generate and store OTP
        otp_record = await self.repo.generate_and_store_otp(
            otp_request.user_id,
            otp_request.organization_id,
            otp_request.phone_number
        )
        
        # TODO: Send OTP to phone number (integrate SMS service like Twilio)
        # await send_sms(otp_request.phone_number, f"Your OTP is: {otp_record.code}")
        
        return {
            "otp_id": otp_record.id,
            "message": "OTP sent successfully"
        }

    async def verify_otp(self, otp_verify: OtpVerifyRequest):
        """
        Verify OTP and update status to verified
        """
        otp_record = await self.repo.verify_otp(
            otp_verify.user_id,
            otp_verify.organization_id,
            otp_verify.phone_number,
            otp_verify.otp_code
        )
        
        if not otp_record:
            raise ValueError("Invalid or expired OTP")
        
        return {
            "verified": True,
            "otp_id": otp_record.id,
            "message": "OTP verified successfully"
        }