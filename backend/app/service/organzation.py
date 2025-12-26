from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.model.organzation import Organization
from app.schema.organization.main import OrganizationResponse

class OrganizationService:    
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_org(self, org_id: int) -> OrganizationResponse:
        result = await self.db.execute(
            select(Organization).where(Organization.id == org_id)
        )
        org = result.scalar_one_or_none()
        if not org:
            raise ValueError("Organization not found")
        return OrganizationResponse.from_orm(org)