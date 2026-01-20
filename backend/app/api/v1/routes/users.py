from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database import get_db
from backend.app.schema.users.main import UserResponse
from backend.app.service.userService import UserService

router=APIRouter()

@router.get("/{org_id}",response_model=list[UserResponse])
async def getAllUsers(db:AsyncSession  = Depends(get_db),org_id:str=""):
  users=await UserService(db).get_all_users(org_id)
  return [UserResponse.model_validate(user) for user in users]
