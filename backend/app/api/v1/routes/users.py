from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.schema.users import UserCreate, UserResponse
from app.service.user import UserService

router = APIRouter()


@router.get("/{org_id}", response_model=list[UserResponse])
async def get_all_users(
    org_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return await UserService(db).get_all_users(org_id)


@router.get("/{user_id}/{org_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: str,
    org_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return await UserService(db).get_user_by_id(user_id, org_id)


@router.delete("/{user_id}/{org_id}")
async def delete_user(
    user_id: str,
    org_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return await UserService(db).delete_user_by_id(user_id, org_id)


@router.post("/", response_model=UserResponse)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return await UserService(db).create_user(user_data)


@router.put("/{user_id}/{org_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    org_id: str,
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return await UserService(db).update_user(user_id, org_id, user_data)
