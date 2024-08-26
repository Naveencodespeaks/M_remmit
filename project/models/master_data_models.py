from sqlalchemy import Column, Integer,INT, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
#Base = declarative_base()
from  .base_model import BaseModel
class MdUserRole(BaseModel):
    __tablename__ = "md_user_roles"
    id = Column(Integer, primary_key=True, autoincrement=True)  # Ensure this is the primary key
    name = Column(Text, index=True)
    user = relationship('UserModel', back_populates='role_details')

    class Config:
        orm_mode = True

class MdUserStatus(BaseModel):
    
    __tablename__ = "md_user_status"
    id = Column(Integer, primary_key=True, autoincrement=True)  # Ensure this is the primary key
    name = Column(Text )
    user_status = relationship('UserModel', back_populates='status_details')

class MdCountries(BaseModel):
    __tablename__ = "md_countries"
    id = Column(Integer, primary_key=True, autoincrement=True)
    shortName = Column(String(100), default='')
    name =   Column(String(100),default='' )
    phoneCode=  Column(Integer,default=None)
    order = Column(Integer,default=None)
    currencySymbol =Column(String(100),default='' )
    currencyCode = Column(String(100),default='' )
    zipcodeLength = Column(Integer, default=None)
    allowNumAndCharInZipcode =Column(String(100),default='' )
    mapName =Column(String(100),default="")
    allowNumAndCharInZipcode = Column(String(100),default='' )

    user_country = relationship("UserModel", back_populates="country_details")




#md_states.json
class MdStates(BaseModel):
    __tablename__ = "md_states"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name =   Column(String(100),default='' )
    mapName=  Column(String(100),default='' )
    countryId = Column(Integer, default=None)

class MdLocations(BaseModel):
    __tablename__ = "md_locations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name =   Column(String(100),default='' )
    stateId=  Column(Integer,default=None)
    countryId = Column(Integer, default=None)


#md_reminder_status
class MdReminderStatus(BaseModel):
    
    __tablename__ = "md_reminder_status"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(55) )
    


#md_task_status.json
class MdTaskStatus(BaseModel):
    __tablename__ = "md_task_status"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(55) )
    

#md_tenant_status
class MdTenantStatus(BaseModel):
    __tablename__ = "md_tenant_status"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(55) )
    

#md_timezone.json
class MdTimeZone(BaseModel):
    __tablename__ = "md_timezones"
    id = Column(Integer, primary_key=True, autoincrement=True)
    zone =  Column(String(55) )
    name = Column(String(55) )

class MdKycstatus(BaseModel):
    __tablename__ = "md_kyc_status"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(55) )
    user_kyc = relationship("UserModel", back_populates="kyc_status")
    
class MdOccupations(BaseModel):
    __tablename__ = "md_occupations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(55) )    





