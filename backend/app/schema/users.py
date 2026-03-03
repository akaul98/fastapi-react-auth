
from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserCreate(BaseModel):
  organization_id:str
  name:str
  email:EmailStr
  phone:Optional[str]
  theme:Optional[str]


class UserResponse(BaseModel):
  id:str
  organization_id:str
  name:str
  email:EmailStr
  phone:Optional[str]
  status:bool
  created_at:datetime
  updated_at:Optional[datetime]
  
  class Config:
    from_attributes = True

  