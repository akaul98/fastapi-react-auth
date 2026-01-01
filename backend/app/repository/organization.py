from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
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
        new_org = Organization(org_data)
        self.db.add(new_org)
        await self.db.commit()
        await self.db.refresh(new_org)
        return new_org
    
    async def get_all_orgs(self) -> list[Organization]:
        result = await self.db.execute(select(Organization).where(Organization.status == True))
        return list(result.scalars().all())
    
    async def delete_org(self, org_id: str) -> None:
        org = await self.get_org_by_id(org_id)
        if org:
            await self.db.execute(update(Organization).where(Organization.id == org_id).values(status=False))
            await self.db.commit()

    async def update_org(self, org_id: str, org_data: OrganizationCreate) -> Organization:
        org = await self.get_org_by_id(org_id)
        if org:
            for key, value in org_data.model_dump().items():
                setattr(org, key, value)
            self.db.add(org)
            await self.db.commit()
            await self.db.refresh(org)
        return org