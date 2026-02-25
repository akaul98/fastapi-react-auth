from typing import Optional
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

"""Common base model mixin used across the project.

Provides timestamp audit columns and a soft-delete status flag so models
do not duplicate boilerplate.

Design notes:
- Keep this as an attribute-only mixin (no DB session logic).
- Business rules (e.g. filtering) belong in repositories/services, not here.
"""


class CommonBase:
    """Base mixin providing common columns for all models.

    Fields provided:
    - `id`: primary key string column
    - `created_at`: timezone-aware timestamp with server default
    - `updated_at`: timezone-aware timestamp updated on change
    - `status`: boolean flag for active/inactive (soft-delete)

    Behavior:
    - `status` defaults to True (active).
    - Set `instance.status = False` to soft-delete without removing the row.
    - Queries should filter with `Model.status == True` to show only active records.

    Example:
        # soft-delete
        org.status = False
        await db.commit()

        # query only active
        await db.execute(select(Organization).where(Organization.status == True))
    """
    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )
    status: Mapped[bool] = mapped_column(Boolean, default=True)
