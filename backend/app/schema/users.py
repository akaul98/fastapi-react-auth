
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime

from app.schema.base import BaseSchema


class UserCreate(BaseSchema):
  organization_id:str
  name:str
  email:EmailStr
  phone:Optional[str]
  theme:Optional[str]

class UserUpdate(BaseSchema):
  name:Optional[str]
  email:Optional[EmailStr]
  phone:Optional[str]
  theme:Optional[str]


class UserResponse(BaseSchema):
  id:str
  organization_id:str
  name:str
  email:EmailStr
  phone:Optional[str]
  status:bool
  created_at:datetime
  updated_at:Optional[datetime]
  theme:Optional[str]

  