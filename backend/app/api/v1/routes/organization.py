from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.database import get_db
from app.schema.organization.main import OrganizationResponse

router = APIRouter()

@router.get("/",response_model=list[OrganizationResponse])
async def list_organizations(db: AsyncSession = Depends(get_db)):
    try:
        return OrganizationService(db).get_org(org_id)
    except ValueError as e:
        raise HTTPException(404, str(e))