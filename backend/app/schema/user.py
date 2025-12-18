from sqlalchemy import Column,String,Boolean,DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.sql import func
from database import Base
from enum import Enum

class ThemeEnum(str,Enum):
  light="light"
  dark="dark"

  
class User(Base):

  __tablename__="users"

  id=Column(String,primary_key=True,index=True)
  email=Column(String, nullable=False)
  phone=Column(String,nullable=False)
  Status=Column(Boolean,default=True,nullable=False)
  Theme=Column(SQLEnum(ThemeEnum),default=ThemeEnum.light,nullable=False)
  created_at=Column(DateTime(timezone=True),server_default=func.now())
  updated_at=Column(DateTime(timezone=True),onupdate=func.now())

  



