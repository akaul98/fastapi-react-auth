from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.model.organization import Organization
from app.schema.organization.main import OrganizationCreate

class OrganizationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_org_by_id(self, org_id: str) -> Organization | None:
        result = await self.db.execute(
            select(Organization).where(Organization.id == org_id)
        )
        return result.scalar_one_or_none()
    
    async def create_org(self, org_data: OrganizationCreate) -> Organization:
        new_org = Organization(**org_data)
        self.db.add(new_org)
        await self.db.commit()
        await self.db.refresh(new_org)
        return new_org