from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.model.common import CommonBase


if TYPE_CHECKING:
    from .user import User


class Organization(CommonBase, Base):
    __tablename__ = "organizations"

    org_code: Mapped[str] = mapped_column(String)
    org_name: Mapped[str] = mapped_column(String)
    org_website: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    users: Mapped[list["User"]] = relationship(
        back_populates="organization",
        cascade="all, delete-orphan"
    )
