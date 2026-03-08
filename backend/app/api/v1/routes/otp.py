from fastapi import APIRouter, Depends, HTTPException, Request, status
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.schema.otp import OtpRequest, OtpVerifyRequest, OtpResponse
from app.service.otp import OtpService
from app.core.limiter import limiter


router = APIRouter()


@router.post("/send", response_model=OtpResponse)
@limiter.limit("3/minute")
async def send_otp(request: Request, otp_request: OtpRequest, db: AsyncSession = Depends(get_db)):
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


@router.post("/verify", response_model=OtpResponse)
@limiter.limit("5/minute")
async def verify_otp(request: Request, otp_verify: OtpVerifyRequest, db: AsyncSession = Depends(get_db)):
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
