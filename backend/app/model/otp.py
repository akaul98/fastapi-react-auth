from app.database import Base
from sqlalchemy import String, Boolean, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timedelta
from enum import Enum
from typing import TYPE_CHECKING
from app.model.common import CommonBase

if TYPE_CHECKING:
    from .user import User


class OTPStatusEnum(str, Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    EXPIRED = "expired"


class OTP(CommonBase, Base):
    __tablename__ = "otp"

    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), index=True)
    organization_id: Mapped[str] = mapped_column(String, ForeignKey("organizations.id"), index=True)
    phone: Mapped[str] = mapped_column(String, index=True)
    code: Mapped[str] = mapped_column(String(5))
    status: Mapped[OTPStatusEnum] = mapped_column(
        SQLEnum(OTPStatusEnum), default=OTPStatusEnum.PENDING
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime)
    verified_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
