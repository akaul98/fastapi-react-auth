import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.model.revoked_token import RevokedToken


class RevokedTokenRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def revoke(self, jti: str, expires_at: datetime) -> None:
        record = RevokedToken()
        record.id = str(uuid.uuid4())
        record.jti = jti
        record.expires_at = expires_at
        self.db.add(record)
        await self.db.commit()

    async def is_revoked(self, jti: str) -> bool:
        result = await self.db.execute(
            select(RevokedToken).where(RevokedToken.jti == jti)
        )
        return result.scalar_one_or_none() is not None
