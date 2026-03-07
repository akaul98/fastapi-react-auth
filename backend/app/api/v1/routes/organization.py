import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.schema.organization import OrganizationCreate, OrganizationResponse
from app.service.organization import OrganizationService

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/{org_id}", response_model=OrganizationResponse)
async def get_organization(
    org_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        return await OrganizationService(db).get_org(org_id)
    except ValueError as e:
        raise HTTPException(404, str(e))


@router.post("/", response_model=OrganizationResponse)
async def create_organization(
    org: OrganizationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        return await OrganizationService(db).create_org(org)
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.get("/", response_model=list[OrganizationResponse])
async def list_organizations(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return await OrganizationService(db).get_all_orgs()


@router.delete("/{org_id}")
async def delete_organization(
    org_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        await OrganizationService(db).delete_org(org_id)
        return {"detail": "Organization deleted"}
    except ValueError as e:
        raise HTTPException(404, str(e))


@router.put("/{org_id}", response_model=OrganizationResponse)
async def update_organization(
    org_id: str,
    org: OrganizationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        return await OrganizationService(db).update_org(org_id, org)
    except ValueError as e:
        raise HTTPException(404, str(e))
