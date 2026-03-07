from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.limiter import limiter
from app.schema.otp import OtpRequest, OtpResponse, OtpVerifyRequest
from app.service.otp import OtpService

router = APIRouter()


@router.post("/send", response_model=OtpResponse)
@limiter.limit("5/minute")
async def send_otp(request: Request, otp_request: OtpRequest, db: AsyncSession = Depends(get_db)):
    try:
        return await OtpService(db).send_otp(otp_request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/verify", response_model=OtpResponse)
@limiter.limit("10/minute")
async def verify_otp(request: Request, otp_verify: OtpVerifyRequest, db: AsyncSession = Depends(get_db)):
    try:
        return await OtpService(db).verify_otp(otp_verify)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
