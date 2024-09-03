from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
#from project.database.database import Base
from datetime import datetime
#Base = declarative_base()
from .base_model import BaseModel

class AdminUser(BaseModel):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(61))
    password = Column(Text)
    login_token = Column(Text)
    token = Column(Text)
    email = Column(String(161))
<<<<<<< HEAD
    mobile_no = Column(String(15))
=======
    mobile_no = Column(String(13))
>>>>>>> 4ff072eea4bf3d9e21bdfa50534e18dd866d673d
    last_login = Column(DateTime, default= datetime.utcnow() )
    role_id = Column(Integer, default=1)  # Ensure this matches UserRole.id
    status_id = Column(Integer, default=3)
    


    class Config:
<<<<<<< HEAD
        from_attributes = True
        str_strip_whitespace = True
=======
        orm_mode = True
>>>>>>> 4ff072eea4bf3d9e21bdfa50534e18dd866d673d
