import logging
from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schema.organization.main import OrganizationCreate, OrganizationResponse
from app.service.organization import OrganizationService

logger = logging.getLogger(__name__)



router = APIRouter()

@router.get("/{org_id}",response_model=OrganizationResponse)
async def list_organizations(db: AsyncSession = Depends(get_db), org_id: str = None):
    logger.info(f"Fetching organization with ID: {org_id}")
    try:
        result = await OrganizationService(db).get_org(org_id)
        logger.debug(f"Organization found: {result}")
        return result
    except ValueError as e:
        logger.error(f"Organization not found: {org_id}, Error: {str(e)}")
        raise HTTPException(404, str(e))
    
@router.post("/",response_model=OrganizationResponse)
async def create_organization(org: OrganizationCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await OrganizationService(db).create_org(org)
    except ValueError as e:
        raise HTTPException(400, str(e))