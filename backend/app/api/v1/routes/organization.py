import logging
from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schema.organization import OrganizationCreate, OrganizationResponse, OrganizationUpdate
from app.schema.auth import CurrentUser
from app.service.organization import OrganizationService
from app.core.dependencies import get_current_user

logger = logging.getLogger(__name__)



router = APIRouter()

@router.get("get_org_list_by_id/{org_id}",response_model=OrganizationResponse)
async def list_organizations(db: AsyncSession = Depends(get_db), org_id: str = "", _: CurrentUser = Depends(get_current_user)):
    try:
        result = await OrganizationService(db).get_org(org_id)
        return result
    except ValueError as e:
        raise HTTPException(404, str(e))

@router.post("create_org",response_model=OrganizationResponse)
async def create_organization(org: OrganizationCreate, db: AsyncSession = Depends(get_db), _: CurrentUser = Depends(get_current_user)):
    try:
        return await OrganizationService(db).create_org(org)
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.get("get_org_list",response_model=list[OrganizationResponse])
async def get_organizations(db: AsyncSession = Depends(get_db), _: CurrentUser = Depends(get_current_user)):
    orgs = await OrganizationService(db).get_all_orgs()
    return [OrganizationResponse.model_validate(org) for org in orgs]

@router.delete("delete_org/{org_id}",response_model=dict)
async def delete_organization(org_id: str, db: AsyncSession = Depends(get_db), _: CurrentUser = Depends(get_current_user)):
    try:
        await OrganizationService(db).delete_org(org_id)
        return {"detail": "Organization deleted"}
    except ValueError as e:
        raise HTTPException(404, str(e))
        raise HTTPException(404, str(e))

@router.put("update_org/{org_id}",response_model=OrganizationResponse)
async def update_organization(org_id: str, org: OrganizationUpdate, db: AsyncSession = Depends(get_db), _: CurrentUser = Depends(get_current_user)):
    try:
        updated_org = await OrganizationService(db).update_org(org_id, org)
        return OrganizationResponse.model_validate(updated_org)
    except ValueError as e:
        raise HTTPException(404, str(e))
        raise HTTPException(404, str(e))