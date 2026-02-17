from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.schema.otp import OtpRequest, OtpVerifyRequest, OtpResponse
from app.service.otp import OtpService


router = APIRouter()


@router.post("/sendOtp", response_model=OtpResponse)
async def send_otp(otp_request: OtpRequest, db: AsyncSession = Depends(get_db)):
    """
    Send OTP endpoint
    - Validates organization and user
    - Generates 5-digit OTP
    - Stores in database
    """
    try:
        result = await OtpService(db).send_otp(otp_request)
        return OtpResponse(
            message=result["message"],
            otp_id=result["otp_id"]
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send OTP: {str(e)}"
        )


@router.post("/verifyOtp", response_model=OtpResponse)
async def verify_otp(otp_verify: OtpVerifyRequest, db: AsyncSession = Depends(get_db)):
    """
    Verify OTP endpoint
    - Validates OTP code
    - Updates OTP status to verified
    - Returns verification result
    """
    try:
        result = await OtpService(db).verify_otp(otp_verify)
        return OtpResponse(
            message=result["message"],
            otp_id=result["otp_id"]
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to verify OTP: {str(e)}"
        )