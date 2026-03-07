
from typing import Optional
from datetime import datetime

from app.schema.base import BaseSchema


class OrganizationCreate(BaseSchema):
  org_code:str
  org_name:str
  org_website:Optional[str]

class OrganizationUpdate(BaseSchema):
  org_code:Optional[str]
  org_name:Optional[str]
  org_website:Optional[str]
  status:Optional[bool]

class OrganizationResponse(BaseSchema):
  id:str
  org_code:str
  org_name:str
  org_website:Optional[str]
  status:bool
  created_at:datetime
  updated_at:Optional[datetime]


  