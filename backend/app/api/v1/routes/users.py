from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schema.users import UserCreate, UserResponse, UserUpdate
from app.schema.auth import CurrentUser
from app.service.user import UserService
from app.core.dependencies import get_current_user

router=APIRouter()

@router.get("get_user_list/{org_id}",response_model=list[UserResponse])
async def get_all_users(db:AsyncSession  = Depends(get_db),org_id:str="", _: CurrentUser = Depends(get_current_user)):
   return await UserService(db).get_all_users(org_id)



@router.get("get_user_by_id/{user_id}/{org_id}",response_model=UserResponse)
async def get_user_by_id(db:AsyncSession  = Depends(get_db),user_id:str="",org_id:str="", _: CurrentUser = Depends(get_current_user)):
  return await  UserService(db).get_user_by_id(user_id,org_id)


@router.delete("delete_user/{user_id}/{org_id}")
async def delete_user_by_id(db:AsyncSession  = Depends(get_db),user_id:str="",org_id:str="", _: CurrentUser = Depends(get_current_user)):
  return await UserService(db).delete_user_by_id(user_id,org_id)


@router.post("create_user",response_model=UserResponse)
async def create_user(user_data:UserCreate, db:AsyncSession  = Depends(get_db), _: CurrentUser = Depends(get_current_user)):
  return await UserService(db).create_user(user_data)

@router.put("update_user/{user_id}/{org_id}",response_model=UserResponse)
async def update_user(user_data:UserUpdate, db:AsyncSession  = Depends(get_db),user_id:str="",org_id:str="", _: CurrentUser = Depends(get_current_user)):
  return await UserService(db).update_user(user_id,org_id,user_data)
  