from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schema.organization.main import OrganizationResponse
from app.service.organization import OrganizationService



router = APIRouter()

@router.get("/{org_id}",response_model=OrganizationResponse)
async def list_organizations(db: AsyncSession = Depends(get_db), org_id: int = None):
    try:
        return OrganizationService(db).get_org(org_id)
    except ValueError as e:
        raise HTTPException(404, str(e))