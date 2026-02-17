from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schema.users import UserCreate, UserResponse
from app.service.userService import UserService

router=APIRouter()

@router.get("/{org_id}",response_model=list[UserResponse])
async def getAllUsers(db:AsyncSession  = Depends(get_db),org_id:str=""):
  users=await UserService(db).get_all_users(org_id)
  return [UserResponse.model_validate(user) for user in users]


@router.get("/getUserById/{user_id}/{org_id}",response_model=UserResponse)
async def getUserById(db:AsyncSession  = Depends(get_db),user_id:str="",org_id:str=""):
  user=await UserService(db).get_user_by_id(user_id,org_id)
  return UserResponse.model_validate(user)


@router.delete("/deleteUserById/{user_id}/{org_id}")
async def deleteUserById(db:AsyncSession  = Depends(get_db),user_id:str="",org_id:str=""):
  user=await UserService(db).delete_user_by_id(user_id,org_id)
  return {"message":"User deleted successfully"}

@router.post("/createUser",response_model=UserResponse)
async def createUser(user_data:UserCreate, db:AsyncSession  = Depends(get_db)):
  user=await UserService(db).create_user(user_data)
  return UserResponse.model_validate(user)

@router.put("/updateUser/{user_id}/{org_id}",response_model=UserResponse)
async def updateUser(user_data:UserCreate, db:AsyncSession  = Depends(get_db),user_id:str="",org_id:str=""):
  return await UserService(db).update_user(user_id,org_id,user_data)
  