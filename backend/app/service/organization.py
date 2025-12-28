
from app.schema.organization.main import OrganizationResponse
from backend.app.repository.organization import OrganizationRepository

class OrganizationService:    
    async def get_org(org_id: int) -> OrganizationResponse:
        org_repo = OrganizationRepository()
        org = await org_repo.get_org_by_id(org_id)
        if not org:
            raise ValueError("Organization not found")
        return OrganizationResponse.from_orm(org)