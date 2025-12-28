from sqlalchemy.ext.asyncio import AsyncSession
from app.schema.organization.main import OrganizationResponse
from app.repository.organization import OrganizationRepository

class OrganizationService:
    def __init__(self, db: AsyncSession):
        self.repo = OrganizationRepository(db)

    async def get_org(self, org_id: int) -> OrganizationResponse:
        org = await self.repo.get_org_by_id(org_id)
        if not org:
            raise ValueError("Organization not found")
        return OrganizationResponse.model_validate(org)
