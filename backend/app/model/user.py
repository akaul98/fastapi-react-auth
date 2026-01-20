from sqlalchemy import String,Boolean,DateTime, ForeignKey
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.sql import func
from app.database import Base
from enum import Enum
from sqlalchemy.orm import Mapped,mapped_column,relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from .organization import Organization

class ThemeEnum(str,Enum):
  light="light"
  dark="dark"

  
class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    organization_id: Mapped[str] = mapped_column(
        ForeignKey("organizations.id"),
        nullable=False
    )
    email: Mapped[str] = mapped_column(String, unique=True)
    phone: Mapped[str] = mapped_column(String)
    status: Mapped[bool] = mapped_column(Boolean, default=True)

    theme: Mapped[ThemeEnum] = mapped_column(
        SQLEnum(ThemeEnum), default=ThemeEnum.light
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )

    organization: Mapped["Organization"] = relationship(
        back_populates="users"
    )

  



