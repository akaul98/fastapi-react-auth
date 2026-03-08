from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schema.auth import LoginRequest, RefreshRequest, TokenResponse
from app.schema.otp import OtpResponse, OtpVerifyRequest
from app.service.auth import AuthService
from app.core.limiter import limiter

router = APIRouter()

@router.post("/login", response_model=OtpResponse)
@limiter.limit("5/minute")
async def login(request: Request, login_data: LoginRequest, db: AsyncSession = Depends(get_db)):
    try:
        result = await AuthService(db).login(login_data)
        return OtpResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/verify", response_model=TokenResponse)
@limiter.limit("5/minute")
async def verify_otp(request: Request, otp_verify: OtpVerifyRequest, db: AsyncSession = Depends(get_db)):
    try:
        result = await AuthService(db).verify_and_generate_tokens(otp_verify)
        return TokenResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/refresh", response_model=TokenResponse)
@limiter.limit("10/minute")
async def refresh_token(request: Request, refresh_request: RefreshRequest, db: AsyncSession = Depends(get_db)):
    try:
        result = await AuthService(db).refresh_token(refresh_request.refresh_token)
        return TokenResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
