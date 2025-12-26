
from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class OrganizationCreate(BaseModel):
  id:str
  org_code:str
  org_name:str
  org_website:Optional[str]
  status:bool

class OrganizationResponse(BaseModel):
  id:str
  org_code:str
  org_name:str
  org_website:Optional[str]
  status:bool
  created_at:datetime
  updated_at:datetime
 
class Config:
  from_attributes = True

  