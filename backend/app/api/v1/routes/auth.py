from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schema.auth import LoginRequest, RefreshRequest, TokenResponse
from app.schema.otp import OtpResponse, OtpVerifyRequest
from app.service.auth import AuthService

router = APIRouter()


@router.post("/login", response_model=OtpResponse)
async def login(login_data: LoginRequest, db: AsyncSession = Depends(get_db)):
    try:
        result = await AuthService(db).login(login_data)
        return OtpResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/verify", response_model=TokenResponse)
async def verify_otp(otp_verify: OtpVerifyRequest, db: AsyncSession = Depends(get_db)):
    try:
        result = await AuthService(db).verify_and_generate_tokens(otp_verify)
        return TokenResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_request: RefreshRequest, db: AsyncSession = Depends(get_db)):
    try:
        result = await AuthService(db).refresh_token(refresh_request.refresh_token)
        return TokenResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
