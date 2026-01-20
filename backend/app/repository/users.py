
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.model.user import User
class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_users(self, org_id: str) -> list[User]:
        result = await self.db.execute(select(User).where(User.status == True and User.organization_id == org_id))
        return list(result.scalars().all())