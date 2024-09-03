from sqlalchemy import Column, Integer,INT, String, Text, DateTime, ForeignKey,Enum,Date,Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
#from project.database.database import Base
#Base = declarative_base()
from  .base_model import BaseModel
from datetime import datetime
from enum import Enum as PyEnum
class kycStatus(PyEnum):
    PENDING = 0
    COMPLETED = 1
<<<<<<< HEAD



class TenantModel(BaseModel):
    __tablename__ = "tenants" 
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), default='')
    email = Column(String(161), nullable=False )
    mobile_no = Column(String(15), default="")
    tenant_user = relationship('UserModel', back_populates='tenant_details')
    
    class Config:
        from_attributes = True
        str_strip_whitespace = True
   
class NotificationModel(BaseModel):
    __tablename__ = "user_notificatuions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(Text)
    is_active = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    tenant_id = Column(Integer, default=None)
    category = Column(String(50), default = None)
    ref_id = Column(Integer,default=None)
    user_details = relationship(
        'UserModel', 
        back_populates='user_notifications',
        foreign_keys=[user_id]
    )
    
    class Config:
        from_attributes = True
        str_strip_whitespace = True
class AdminNotificationModel(BaseModel):
    __tablename__ = "admin_notificatuions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    admin_id = Column(Integer, ForeignKey("admin.id"), unique=False, index=True)
    user_id = Column(Integer,ForeignKey("users.id"), index=True)
    category = Column(String(50), default = None)
    ref_id = Column(Integer,default=None)
    user_details = relationship(
        'UserModel', 
        back_populates='admin_notificatuions',
        foreign_keys=[user_id]
    )
    

    
    class Config:
        from_attributes = True
        str_strip_whitespace = True
   
=======
    

>>>>>>> 4ff072eea4bf3d9e21bdfa50534e18dd866d673d
class UserModel(BaseModel):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    name = Column(String(150), default='')
    password = Column(Text)
    token = Column(Text)
    email = Column(String(161), nullable=False )
    mobile_no = Column(String(15), default="")
    
    date_of_birth = Column(Date, nullable=True) 
    last_login = Column(DateTime, default= datetime.utcnow() )
     
    login_fail_count =  Column(Integer, default=0,comment='User Login Fail count')
    login_attempt_date = Column(DateTime, default= None,comment='Last Login Attempt date' )
    otp=Column(String(61))
<<<<<<< HEAD
    #tenant_id = Column(Integer, nullable=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), default=None, unique=False, index=True)
    tenant_details = relationship('TenantModel', back_populates='tenant_user')

=======
    tenant_id = Column(Integer, nullable=True)
>>>>>>> 4ff072eea4bf3d9e21bdfa50534e18dd866d673d
    role_id = Column(Integer, ForeignKey('md_user_roles.id'), nullable=False,default=1)  # Ensure this matches UserRole.id
    role_details = relationship('MdUserRole', back_populates='user')
    status_id = Column(Integer, ForeignKey('md_user_status.id'),  nullable=False,default=1)
    status_details = relationship('MdUserStatus', back_populates='user_status')

    user_details = relationship("UserDetails", back_populates="user")

    country_id = Column(Integer, ForeignKey("md_countries.id"), nullable=False, default=None )
    country_details = relationship("MdCountries", back_populates="user_country")
    

    state_id = Column(Integer, ForeignKey("md_states.id"), nullable=True, default=None )
    location_id = Column(Integer, ForeignKey("md_locations.id"), nullable=True, index=True )

    #KYC STATUS
    kyc_status_id = Column(Integer, ForeignKey("md_kyc_status.id"), nullable=False, default=1 )
    kyc_status = relationship("MdKycstatus", back_populates="user_kyc")
    
<<<<<<< HEAD
    user_notifications = relationship(
        'NotificationModel', 
        back_populates='user_details',
        foreign_keys='NotificationModel.user_id'
    )
    admin_notificatuions = relationship(
        'AdminNotificationModel', 
        back_populates='user_details',
        foreign_keys='AdminNotificationModel.user_id'
    )
=======
    
>>>>>>> 4ff072eea4bf3d9e21bdfa50534e18dd866d673d

    accepted_terms = Column(Boolean, default=False)

    class Config:
<<<<<<< HEAD
        from_attributes = True
        str_strip_whitespace = True
=======
        orm_mode = True
>>>>>>> 4ff072eea4bf3d9e21bdfa50534e18dd866d673d

class UserDetails(BaseModel):
    __tablename__ = "user_detais"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id =  Column(Integer, ForeignKey("users.id"), nullable=False, index=True,unique=True )
<<<<<<< HEAD
    street = Column(Text)
    city = Column(Text)
    state = Column(Text)
    pincode = Column(String(50))
    occupation=Column(String(50))
    annual_income=Column(Integer)
    #occupation_id = Column(Integer, ForeignKey("md_occupations.id"), nullable=False, default=None )
    #occupation_details = relationship("MdOccupations", back_populates="user_occuption")
    
    user = relationship("UserModel", back_populates="user_details")



class BeneficiaryModel(BaseModel):
    __tablename__ = "beneficiaries"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=False, index=True)

    full_name = Column(String(50), index=True)
    short_name = Column(String(50), default="")
    email = Column(String(161), nullable=True )
    mobile_no = Column(String(15), nullable=True)
    
    country_id = Column(Integer, ForeignKey("md_countries.id"), nullable=False)
    beneficiary_country_details = relationship(
        "MdCountries", 
        back_populates="beneficiary_country",
        foreign_keys=[country_id]
    )
    
    city = Column(String(50), index=True)
    state_province = Column(String(50))
    postal_code = Column(String(50))
    swift_code = Column(String(15))
    iban = Column(String(15))
    bank_name = Column(String(50))
    
    bank_country_id = Column(Integer, ForeignKey("md_countries.id"), nullable=False)
    beneficiary_bank_country_details = relationship(
        "MdCountries", 
        back_populates="beneficiary_bank_country",
        foreign_keys=[bank_country_id]
    )
    
    bank_address = Column(String(1500))
    status_id = Column(Integer, ForeignKey("md_beneficiary_status.id"), nullable=False)
    status_details = relationship(
        "MdBeneficiaryStatus",
        back_populates="beneficiary_status_details",
        foreign_keys=[status_id]
    )





=======
    user = relationship("UserModel", back_populates="user_details")

    
>>>>>>> 4ff072eea4bf3d9e21bdfa50534e18dd866d673d
