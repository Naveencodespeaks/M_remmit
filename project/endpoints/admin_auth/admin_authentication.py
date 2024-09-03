from datetime import datetime, timezone
from sqlalchemy import and_
from datetime import datetime
from ...models.admin_user import AdminUser
from ...models.master_data_models import MdUserRole,MdUserStatus

from . import APIRouter, Utility, SUCCESS, FAIL, EXCEPTION ,INTERNAL_ERROR,BAD_REQUEST,BUSINESS_LOGIG_ERROR, Depends, Session, get_database_session, AuthHandler
from ...schemas.register import AdminRegister
import re
from ...schemas.login import Login
import os
import json
from pathlib import Path
from ...models.master_data_models import MdCountries,MdLocations,MdReminderStatus,MdStates,MdTaskStatus,MdTenantStatus,MdTimeZone,MdUserRole,MdUserStatus
# APIRouter creates path operations for product module
router = APIRouter(
    prefix="/Admin",
    tags=["Admin Authentication"],
    responses={404: {"description": "Not found"}},
)

@router.post("/admin-register", response_description="Admin User Registration")
async def register(request: AdminRegister, db: Session = Depends(get_database_session)):
    try:
        user_name = request.user_name
        contact = request.mobile_no
        email = request.email
        password = request.password
        if user_name == '' or contact == '' or email == '' or password == '':
            return Utility.json_response(status=FAIL, message="Provide valid detail's", error=[], data={})
        if user_name is None or contact is None or email is None or password is None:
            return Utility.json_response(status=FAIL, message="Provide valid detail's", error=[], data={})
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.fullmatch(email_regex, email):
            return Utility.json_response(status=FAIL, message="Provide valid email", error=[], data={})
        # contact_digits = math.floor(math.log10(contact)) + 1
        if len(str(contact)) < 7 or len(str(contact)) > 15:
            return Utility.json_response(status=FAIL, message="Mobile number not valid. Length must be 7-13.",
                                         error=[], data={})
        user_with_email = db.query(AdminUser).filter(AdminUser.email == email).all()
        if len(user_with_email) != 0:
            return Utility.json_response(status=FAIL, message="Email already exists", error=[], data={})

        user_data = AdminUser(role_id =1,status_id=3, email=email,user_name=user_name, mobile_no=contact,password=AuthHandler().get_password_hash(str(password)))
        db.add(user_data)
        db.flush()
        db.commit()
        
        if user_data.id:
            return Utility.json_response(status=SUCCESS, message="Admin Registered Successfully", error=[],
                                         data={"user_id": user_data.id})
        else:
            return Utility.json_response(status=FAIL, message="Something went wrong", error=[], data={})
    except Exception as E:
        print(E)
        db.rollback()
        return Utility.json_response(status=FAIL, message="Something went wrong", error=[], data={})


@router.post("/login", response_description="Admin authenticated")
async def admin_login(request: Login, db: Session = Depends(get_database_session)):
    try:
        email = request.email
        password = request.password
        user = db.query(AdminUser,
                        #AdminUser.email,
                        #AdminUser.status_id,
                        #AdminUser.user_name,
                        #AdminUser.login_token,
                        #AdminUser.password,
                        #AdminUser.id
                        ).filter(AdminUser.email == email)
        if user.count() != 1:
            return Utility.json_response(status=FAIL, message="Invalid credential's", error=[], data={})
        if user.one().status_id !=3:
            msg = "Admin Profile is Deleted"
            if user.one().status_id == 1:
                msg = "Admin Profile is Pending State"
            if user.one().status_id == 2:
                msg = "Admin Profile is Pending State"
            if user.one().status_id == 4:
                msg = "Admin Profile is Inactive State"    
            if user.one().status_id == 5:
                msg = "Admin Profile is Delete"
            return Utility.json_response(status=FAIL, message=msg, error=[], data={})
        user_data = user.one()
        verify_password = AuthHandler().verify_password(str(password), user_data.password)

        if not verify_password:
            return Utility.json_response(status=FAIL, message=verify_password, error=[], data={})
        user_dict = {c.name: getattr(user_data, c.name) for c in user_data.__table__.columns}
        #print(user_dict)
        if "password" in user_dict:
            del user_dict["password"]
        if "token" in user_dict:
            del user_dict["token"]
        login_token = AuthHandler().encode_token(user_dict)
        
        if not login_token:
            return Utility.json_response(status=FAIL, message="Token not assigned", error=[], data={})
        user.update({AdminUser.token: login_token, AdminUser.last_login:datetime.utcnow()}, synchronize_session=False)
        db.flush()
        db.commit()
        
        #print(user_data.status_details)
        #print(user_data.role)
        user_data.token = login_token
        del user_data.password
        del user_data.login_token
        user_dict["token"] = login_token
        return Utility.dict_response(status=SUCCESS, message="Logged in successfully", error=[], data=user_dict)
    except Exception as E:
        print(E)
        db.rollback()
        return Utility.json_response(status=EXCEPTION, message="Something went wrong", error=[], data={})

@router.get("/get-users", response_description="User List")
def get_users(auth_user=Depends(AuthHandler().auth_wrapper), db: Session = Depends(get_database_session)):
    try:
        return Utility.dict_response(status=SUCCESS, message="SUCCESS", error=[], data={})
    except Exception as E:
        print(E)
        return Utility.json_response(status=FAIL, message="Something went wrong", error=[], data={})


# admin_authentication.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum as SQLAEnum, Boolean
from sqlalchemy.orm import relationship, sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from enum import Enum
from datetime import datetime

DATABASE_URL = "mysql+pymysql://remit_admin:remit_admin@127.0.0.1/remit"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class KYCStatus(Enum):
    PENDING = 1
    APPROVED = 2
    REJECTED = 3


class User(Base):
    __tablename__ = 'users'  # Ensure this matches the actual table name

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    name = Column(String(100), nullable=True)  # Assuming 'name' is a full name or display name
    password = Column(String(255), nullable=True)
    token = Column(String(255), nullable=True)
    email = Column(String(100), unique=True, nullable=True)
    mobile_no = Column(String(20), nullable=True)
    date_of_birth = Column(DateTime, nullable=True)
    last_login = Column(DateTime, nullable=True)
    login_fail_count = Column(Integer, default=0)
    login_attempt_date = Column(DateTime, nullable=True)
    otp = Column(String(6), nullable=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=True)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=True)
    status_id = Column(Integer, ForeignKey('statuses.id'), nullable=True)
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=True)
    state_id = Column(Integer, ForeignKey('states.id'), nullable=True)
    location_id = Column(Integer, ForeignKey('locations.id'), nullable=True)
    kyc_status_id = Column(Integer, ForeignKey('kyc_statuses.id'), nullable=True)
    accepted_terms = Column(Boolean, default=False)
    created_on = Column(DateTime, default=datetime.utcnow)
    updated_on = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Define relationships if needed
    kyc = relationship("KYC", back_populates="user")

class Admin(Base):
    __tablename__ = 'admin'

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(61), unique=True, nullable=True)  # Adjusted column name
    kyc_reviews = relationship("KYC", back_populates="admin")


class KYC(Base):
    __tablename__ = 'kyc'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    document_url = Column(String(255), nullable=False)
    status = Column(SQLAEnum(KYCStatus), default=KYCStatus.PENDING, nullable=False)
    submission_date = Column(DateTime, default=datetime.utcnow)
    review_date = Column(DateTime)
    admin_id = Column(Integer, ForeignKey('admin.id'))
    user = relationship("User", back_populates="kyc")
    admin = relationship("Admin", back_populates="kyc_reviews")


Base.metadata.create_all(bind=engine)

