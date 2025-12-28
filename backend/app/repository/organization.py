from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.model.organization import Organization

class OrganizationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_org_by_id(self, org_id: int) -> Organization | None:
        result = await self.db.execute(
            select(Organization).where(Organization.id == org_id)
        )
        return result.scalar_one_or_none()