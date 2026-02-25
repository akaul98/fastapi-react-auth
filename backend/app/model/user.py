from sqlalchemy import String,Boolean,DateTime, ForeignKey
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.sql import func
from app.database import Base
from enum import Enum
from sqlalchemy.orm import Mapped,mapped_column,relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from app.model.common import CommonBase

if TYPE_CHECKING:
    from .organization import Organization

class ThemeEnum(str,Enum):
  light="light"
  dark="dark"

  
class User(CommonBase, Base):
    __tablename__ = "users"

    organization_id: Mapped[str] = mapped_column(
        ForeignKey("organizations.id"),
        nullable=False
    )
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
    phone: Mapped[str] = mapped_column(String)
    theme: Mapped[ThemeEnum] = mapped_column(
        SQLEnum(ThemeEnum), default=ThemeEnum.light
    )

    organization: Mapped["Organization"] = relationship(
        back_populates="users"
    )

  



