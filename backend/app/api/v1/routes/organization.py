import logging
from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schema.organization.main import OrganizationCreate, OrganizationResponse
from app.service.organization import OrganizationService

logger = logging.getLogger(__name__)



router = APIRouter()

@router.get("/{org_id}",response_model=OrganizationResponse)
async def list_organizations(db: AsyncSession = Depends(get_db), org_id: str = ""):
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
    

@router.get("/",response_model=list[OrganizationResponse])
async def get_organizations(db: AsyncSession = Depends(get_db)):
    logger.info("Fetching all organizations")
    orgs = await OrganizationService(db).repo.get_all_orgs()
    logger.debug(f"Organizations found: {orgs}")
    return [OrganizationResponse.model_validate(org) for org in orgs]

@router.delete("/{org_id}",response_model=dict)
async def delete_organization(org_id: str, db: AsyncSession = Depends(get_db)):
    logger.info(f"Deleting organization with ID: {org_id}")
    try:
        await OrganizationService(db).repo.delete_org(org_id)
        logger.debug(f"Organization deleted: {org_id}")
        return {"detail": "Organization deleted"}
    except ValueError as e:
        logger.error(f"Error deleting organization with ID: {org_id}, Error: {str(e)}")
        raise HTTPException(404, str(e))
    
@router.put("/{org_id}",response_model=OrganizationResponse)
async def update_organization(org_id: str, org: OrganizationCreate, db: AsyncSession = Depends(get_db)):
    logger.info(f"Updating organization with ID: {org_id}")
    try:
        updated_org = await OrganizationService(db).repo.update_org(org_id, org)
        logger.debug(f"Organization updated: {updated_org}")
        return OrganizationResponse.model_validate(updated_org)
    except ValueError as e:
        logger.error(f"Error updating organization with ID: {org_id}, Error: {str(e)}")
        raise HTTPException(404, str(e))