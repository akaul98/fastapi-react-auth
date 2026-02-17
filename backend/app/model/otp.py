from app.database import Base
from sqlalchemy import String, Boolean, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timedelta
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


class OTPStatusEnum(str, Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    EXPIRED = "expired"


class OTP(Base):
    __tablename__ = "otp"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), index=True)
    organization_id: Mapped[str] = mapped_column(String, ForeignKey("organizations.id"), index=True)
    phone: Mapped[str] = mapped_column(String, index=True)
    code: Mapped[str] = mapped_column(String(5))
    status: Mapped[OTPStatusEnum] = mapped_column(
        SQLEnum(OTPStatusEnum), default=OTPStatusEnum.PENDING
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime)
    verified_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
