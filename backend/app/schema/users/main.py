
from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
  id:str
  organization_id:str
  email:str
  phone:Optional[str]
  status:bool
  theme:Optional[str]


class UserResponse(BaseModel):
  id:str
  organization_id:str
  email:str
  phone:Optional[str]
  status:bool
  created_at:datetime
  updated_at:Optional[datetime]
  
  class Config:
    from_attributes = True

  