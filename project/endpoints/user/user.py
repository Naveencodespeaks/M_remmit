from datetime import datetime, timezone,timedelta
from datetime import datetime
<<<<<<< HEAD
from ...models.user_model import UserModel,UserDetails,BeneficiaryModel
from ...models.master_data_models import MdUserRole,MdUserStatus,MdCountries

from . import APIRouter, Utility, SUCCESS, FAIL, EXCEPTION ,INTERNAL_ERROR,BAD_REQUEST,BUSINESS_LOGIG_ERROR, Depends, Session, get_database_session, AuthHandler
from ...schemas.user_schema import UpdatePassword,UserFilterRequest,PaginatedUserResponse,PaginatedBeneficiaryResponse,BeneficiaryListReq,GetUserDetailsReq,UserListResponse, UpdateUserDetails,UpdateProfile,BeneficiaryRequest,BeneficiaryEdit, GetBeneficiaryDetails, ActivateBeneficiary,UpdateBeneficiaryStatus, ResendBeneficiaryOtp,BeneficiaryResponse
=======
from ...models.user_model import UserModel
from ...models.master_data_models import MdUserRole,MdUserStatus,MdCountries

from . import APIRouter, Utility, SUCCESS, FAIL, EXCEPTION ,INTERNAL_ERROR,BAD_REQUEST,BUSINESS_LOGIG_ERROR, Depends, Session, get_database_session, AuthHandler
from ...schemas.user_schema import UpdatePassword,UsersList,UserResponse,UpdateProfile
>>>>>>> 4ff072eea4bf3d9e21bdfa50534e18dd866d673d
import re
from ...constant import messages as all_messages
from ...common.mail import Email
from sqlalchemy.sql import select, and_, or_, not_,func
from sqlalchemy.future import select
from datetime import date, datetime
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey, func
from sqlalchemy.ext.asyncio import AsyncSession
<<<<<<< HEAD
from ...models.admin_configuration_model import tokensModel
from sqlalchemy import desc, asc
from typing import List
from fastapi import BackgroundTasks
from fastapi_pagination import Params,paginate 
from sqlalchemy.orm import  joinedload
=======
>>>>>>> 4ff072eea4bf3d9e21bdfa50534e18dd866d673d


# APIRouter creates path operations for product module
router = APIRouter(
    prefix="/user",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)

@router.post("/update-profile", response_description="Update Profile")
async def update_profile(request: UpdateProfile,auth_user=Depends(AuthHandler().auth_wrapper), db: Session = Depends(get_database_session)):
    try:
        
        user_id = auth_user["id"]
        first_name = request.first_name
        last_name = request.last_name
        date_of_birth = request.date_of_birth #Utility.convert_dtring_to_date(request.date_of_birth)
        mobile_no = request.mobile_no

        user_data = db.query(UserModel).filter(UserModel.id == user_id).first()
        if user_data is None:
            return Utility.json_response(status=BUSINESS_LOGIG_ERROR, message=all_messages.USER_NOT_EXISTS, error=[], data={},code="INVALIED_TOKEN")
        if user_data.role_id !=2:
            
            return Utility.json_response(status=BUSINESS_LOGIG_ERROR, message=all_messages.NO_PERMISSIONS, error=[], data={},code="LOGOUT_ACCOUNT")

        else:
            
            if user_data.status_id ==3:                
                user_data.first_name = first_name
                user_data.last_name = last_name
                user_data.name = f'''{first_name} {last_name}'''
                user_data.date_of_birth = date_of_birth
                user_data.mobile_no = mobile_no
                db.commit()
                db.flush(UserModel)
                res_data = {
                    "first_name":user_data.first_name,
                    "last_name":user_data.last_name,
                    "date_of_birth":user_data.date_of_birth,
                    "mobile_no":user_data.mobile_no,
                }

                return Utility.json_response(status=SUCCESS, message=all_messages.PROFILE_UPDATE_SUCCESS, error=[], data={},code="")
            elif  user_data.status_id == 1:
                return Utility.json_response(status=BUSINESS_LOGIG_ERROR, message=all_messages.PENDING_PROFILE_COMPLATION, error=[], data={},code="LOGOUT_ACCOUNT")
            elif  user_data.status_id == 2:
                return Utility.json_response(status=BUSINESS_LOGIG_ERROR, message=all_messages.PENDING_EMAIL_VERIFICATION, error=[], data={},code="LOGOUT_ACCOUNT")
            elif user_data.status_id == 3:
                return Utility.json_response(status=BUSINESS_LOGIG_ERROR, message=all_messages.PROFILE_INACTIVE, error=[], data={},code="LOGOUT_ACCOUNT")
            elif user_data.status_id == 4:
                return Utility.json_response(status=BUSINESS_LOGIG_ERROR, message=all_messages.PROFILE_DELETED, error=[], data={},code="LOGOUT_ACCOUNT")
            else:
                db.rollback()
                return Utility.json_response(status=INTERNAL_ERROR, message=all_messages.SOMTHING_WRONG, error=[], data={})

    except Exception as E:
        print(E)
        db.rollback()
        return Utility.json_response(status=INTERNAL_ERROR, message=all_messages.SOMTHING_WRONG, error=[], data={})

@router.post("/update-password", response_description="Update Password")
async def update_password(request: UpdatePassword,auth_user=Depends(AuthHandler().auth_wrapper), db: Session = Depends(get_database_session)):
    try:
        
        user_id = auth_user["id"]
        old_password = str(request.old_password)
        password =  request.password
        user_data = db.query(UserModel).filter(UserModel.id == user_id).first()
        if user_data is None:
            return Utility.json_response(status=BUSINESS_LOGIG_ERROR, message=all_messages.USER_NOT_EXISTS, error=[], data={},code="USER_NOT_EXISTS")
        else:
            
            verify_password = AuthHandler().verify_password(str(old_password), user_data.password)
            if not verify_password:
                return Utility.json_response(status=BUSINESS_LOGIG_ERROR, message=all_messages.INVALIED_OLD_PASSWORD, error=[], data={})
            if user_data.status_id ==3:
                has_password = AuthHandler().get_password_hash(password)
                user_data.password = has_password
                db.commit()
                #db.flush(user_obj) ## Optionally, refresh the instance from the database to get the updated values
                  #Email.send_mail(recipient_email=[user_obj.email], subject="Reset Password OTP", template='',data=mail_data )
                return Utility.json_response(status=SUCCESS, message=all_messages.UPDATE_PASSWORD_SUCCESS, error=[], data={},code="")
            elif  user_data.status_id == 1:
                return Utility.json_response(status=BUSINESS_LOGIG_ERROR, message=all_messages.PENDING_PROFILE_COMPLATION, error=[], data={},code="LOGOUT_ACCOUNT")
            elif  user_data.status_id == 2:
                return Utility.json_response(status=BUSINESS_LOGIG_ERROR, message=all_messages.PENDING_EMAIL_VERIFICATION, error=[], data={},code="LOGOUT_ACCOUNT")
            elif user_data.status_id == 3:
                return Utility.json_response(status=BUSINESS_LOGIG_ERROR, message=all_messages.PROFILE_INACTIVE, error=[], data={},code="LOGOUT_ACCOUNT")
            elif user_data.status_id == 4:
                return Utility.json_response(status=BUSINESS_LOGIG_ERROR, message=all_messages.PROFILE_DELETED, error=[], data={},code="LOGOUT_ACCOUNT")
            else:
                db.rollback()
                return Utility.json_response(status=INTERNAL_ERROR, message=all_messages.SOMTHING_WRONG, error=[], data={})

    except Exception as E:
        print(E)
        db.rollback()
        return Utility.json_response(status=INTERNAL_ERROR, message=all_messages.SOMTHING_WRONG, error=[], data={})

<<<<<<< HEAD
'''
@router.post("/update-details", response_description="Update Profile")
async def update_details(request: UpdateUserDetails,auth_user=Depends(AuthHandler().auth_wrapper), db: Session = Depends(get_database_session)):
    try:        
        
        user_id = auth_user["id"]
        street = request.street
        city = request.city
        state = request.state
        occupation = request.occupation
        annual_income = request.annual_income
        pincode = request.pincode
        user_obj = db.query(UserModel).filter(UserModel.id == user_id).first()
        if user_obj is None:
            return Utility.json_response(status=BUSINESS_LOGIG_ERROR, message=all_messages.USER_NOT_EXISTS, error=[], data={},code="INVALIED_TOKEN")
        elif user_obj.role_id !=2:
            
            return Utility.json_response(status=BUSINESS_LOGIG_ERROR, message=all_messages.NO_PERMISSIONS, error=[], data={},code="LOGOUT_ACCOUNT")
        if user_obj.status_id == 2:            
            return Utility.json_response(status=BUSINESS_LOGIG_ERROR, message=all_messages.PENDING_EMAIL_VERIFICATION, error=[], data={},code="LOGOUT_ACCOUNT")
    
        elif user_obj.status_id == 4:
            return Utility.json_response(status=BUSINESS_LOGIG_ERROR, message=all_messages.PROFILE_INACTIVE, error=[], data={},code="LOGOUT_ACCOUNT")
        elif user_obj.status_id == 5:
            return Utility.json_response(status=BUSINESS_LOGIG_ERROR, message=all_messages.PROFILE_DELETED, error=[], data={},code="LOGOUT_ACCOUNT")
        
        
        user_details = db.query(UserDetails).filter(UserDetails.user_id == user_id).first()
        if user_details is None:
            details = UserDetails(user_id=user_id,street =street,city=city, state=state,occupation=occupation,annual_income=annual_income,pincode=pincode)
            db.add(details)
            db.flush()
            db.commit()
            return Utility.json_response(status=SUCCESS, message=all_messages.KYC_UPDATE_SUCCESS, error=[], data={},code="")
        else:           
                       
            user_details.street = street
            user_details.city = city
            user_details.state = state
            user_details.occupation = occupation
            user_details.annual_income =annual_income
            user_details.pincode = pincode
            db.commit()
            db.flush(UserModel)
            return Utility.json_response(status=SUCCESS, message=all_messages.KYC_UPDATE_SUCCESS, error=[], data={},code="")
        
    except Exception as E:
        print(E)
        db.rollback()
        return Utility.json_response(status=INTERNAL_ERROR, message=all_messages.SOMTHING_WRONG, error=[], data={})
'''
=======
>>>>>>> 4ff072eea4bf3d9e21bdfa50534e18dd866d673d
def serialize_model(instance):
    """Convert SQLAlchemy ORM model instance to dictionary."""
    return {column.name: getattr(instance, column.name) for column in instance.__table__.columns}

<<<<<<< HEAD

@router.post("/list", response_model=PaginatedUserResponse, response_description="Fetch Users List")
async def get_users(filter_data: UserFilterRequest,auth_user=Depends(AuthHandler().auth_wrapper),db: Session = Depends(get_database_session)):
    #user_obj = db.query(UserModel).filter(UserModel.id == user_id).first()
    #AuthHandler().user_validate(user_obj)
    if auth_user.get("role_id", -1) not in [1]:
        return Utility.json_response(status=BUSINESS_LOGIG_ERROR, message=all_messages.NO_PERMISSIONS, error=[], data={},code="NO_PERMISSIONS")

    
    query = db.query(UserModel).options(
        joinedload(UserModel.tenant_details),
        joinedload(UserModel.role_details),
        joinedload(UserModel.status_details),
        joinedload(UserModel.country_details),
        #joinedload(UserModel.state_details),
        #joinedload(UserModel.location_details),
        joinedload(UserModel.kyc_status)
    )

    if filter_data.search_string:
        search = f"%{filter_data.search_string}%"
        query = query.filter(
            or_(
                UserModel.first_name.ilike(search),
                UserModel.last_name.ilike(search),
                UserModel.email.ilike(search),
                UserModel.mobile_no.ilike(search)
            )
        )
    if filter_data.tenant_id:
        query = query.filter(UserModel.tenant_id.in_(filter_data.tenant_id))

    #if filter_data.role_id:
        #query = query.filter(UserModel.role_id == filter_data.role_id)
    if filter_data.status_ids:
        query = query.filter(UserModel.status_id.in_(filter_data.status_ids))
    if filter_data.country_id:
        query = query.filter(UserModel.country_id.in_(filter_data.country_id))
    if filter_data.kyc_status_id:
        query = query.filter(UserModel.kyc_status_id.in_(filter_data.kyc_status_id))
    if filter_data.start_date and filter_data.end_date and ( isinstance(filter_data.start_date, date) and isinstance(filter_data.end_date, date)):
        query = query.filter(UserModel.created_on > filter_data.start_date)
        query = query.filter(UserModel.created_on < filter_data.end_date)
      
     # Total count of users matching the filters
    total_count = query.count()
    sort_column = getattr(UserModel, filter_data.sort_by, None)
    if sort_column:
        if filter_data.sort_order == "desc":
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc("created_on"))

    # Apply pagination
    offset = (filter_data.page - 1) * filter_data.per_page
    paginated_query = query.offset(offset).limit(filter_data.per_page).all()
    # Create a paginated response
    return PaginatedUserResponse(
        total_count=total_count,
        list=paginated_query,
        page=filter_data.page,
        per_page=filter_data.per_page
    )
@router.post("/get-user-details",response_model=UserListResponse, response_description="Get User Details")
async def get_benficiary( request: GetUserDetailsReq,auth_user=Depends(AuthHandler().auth_wrapper), db: Session = Depends(get_database_session)):
    try:
        
        user_id = auth_user["id"]
        if auth_user.get("role_id", -1) in [1]:
            user_id = request.user_id
        elif auth_user.get("role_id", -1) in [2]:
            user_id = auth_user["id"]
        if auth_user.get("role_id", -1) in [2] and user_id !=request.user_id:
            return Utility.json_response(status=INTERNAL_ERROR, message=all_messages.NO_PERMISSIONS, error=[], data={})

        user_obj = db.query(UserModel).filter(UserModel.id == user_id).first()
        response_data = Utility.model_to_dict(user_obj)
        response_data["user_id"] = response_data["id"]
        response_data["tenant_details"] = Utility.model_to_dict(user_obj.tenant_details)
        response_data["role_details"] = Utility.model_to_dict(user_obj.role_details)
        response_data["status_details"] = Utility.model_to_dict(user_obj.status_details)
        response_data["country_details"] = Utility.model_to_dict(user_obj.country_details)
        response_data["kyc_status"] = Utility.model_to_dict(user_obj.kyc_status)
        if "login_fail_count" in response_data:
            del response_data["login_fail_count"]
        if "password" in response_data:
            del response_data["password"]
        if "otp" in response_data:
            del response_data["otp"]
        if "login_attempt_date" in response_data:
            del response_data["login_attempt_date"]    
                
        return Utility.json_response(status=SUCCESS, message="User Details successfully retrieved", error=[], data=response_data,code="")

    except Exception as E:
        print(E)
        db.rollback()
        return Utility.json_response(status=INTERNAL_ERROR, message=all_messages.SOMTHING_WRONG, error=[], data={})

@router.post("/add-benficiary", response_description="Add Benficiary")
async def add_benficiary(request: BeneficiaryRequest, background_tasks: BackgroundTasks,auth_user=Depends(AuthHandler().auth_wrapper), db: Session = Depends(get_database_session)):
    try:
        user_id = auth_user["id"]
        full_name = request.full_name

        mobile_no = request.mobile_no
        email = request.email
        country_id = request.country_id
        city = request.city
        state_province = request.state_province
        postal_code = request.postal_code
        swift_code = request.swift_code
        iban = request.iban
        bank_name = request.bank_name
        bank_country_id = request.bank_country_id
        bank_address = request.bank_address
               
        user_obj = db.query(UserModel).filter(UserModel.id == user_id).first()
        if user_obj is None:            
            return Utility.json_response(status=500, message=all_messages.USER_NOT_EXISTS, error=[], data={},code="LOGOUT_ACCOUNT")            
        elif user_obj.role_id !=2:            
            return Utility.json_response(status=500, message=all_messages.NO_PERMISSIONS, error=[], data={},code="LOGOUT_ACCOUNT")            
        elif user_obj.status_id == 2:
            return Utility.json_response(status=500, message=all_messages.PENDING_EMAIL_VERIFICATION, error=[], data={},code="LOGOUT_ACCOUNT")            
        elif user_obj.status_id == 4:
            return Utility.json_response(status=500, message=all_messages.PROFILE_INACTIVE, error=[], data={},code="LOGOUT_ACCOUNT")            
        elif user_obj.status_id == 5:
            return Utility.json_response(status=500, message=all_messages.PROFILE_DELETED, error=[], data={},code="LOGOUT_ACCOUNT")
            
        exists_ben = db.query(BeneficiaryModel).filter(BeneficiaryModel.iban == iban,BeneficiaryModel.user_id==user_id).first()
        if exists_ben is not None:
            return Utility.json_response(status=BUSINESS_LOGIG_ERROR, message=all_messages.BENEFICIARY_ALREADY_EXISTS, error=[], data={},code="BENEFICIARY_ALREADY_EXISTS")
        otp =Utility.generate_otp()
        
        details = BeneficiaryModel(user_id=user_id,
                                   full_name =full_name,
                                   mobile_no =mobile_no,
                                   email=email,
                                   city=city,
                                   country_id=country_id,
                                   state_province=state_province,
                                   postal_code=postal_code,
                                   swift_code=swift_code,
                                   iban=iban,
                                   bank_name=bank_name,
                                   bank_country_id=bank_country_id,
                                   bank_address=bank_address,
                                   status_id=1
                                   )
        db.add(details)
        db.commit()
        
        #db.flush()
        if details.id:
            mail_data = {"otp":str(otp),"name":user_obj.first_name +" "+user_obj.last_name,"beneficiary_name":full_name}
            background_tasks.add_task(
            Email.send_mail,
            recipient_email=[user_obj.email],
            subject=all_messages.BENEFICIARY_CREATE_SUCCESS,
            template='beneficiary_beneficiary_added.html',
            data=mail_data
           )
            
            otpdata = { "ref_id":details.id,"catrgory":"BeneficiaryModel","otp":otp,"user_id":user_id,"token":'' }
            otpdata["token"] = AuthHandler().encode_token(otpdata,minutes=6)
            token_data = tokensModel(ref_id=details.id,token=otpdata["token"],catrgory="BeneficiaryModel",user_id=user_id,otp=otp,active=True)
            db.add(token_data)
            db.commit()
            if token_data.id:
                return Utility.json_response(status=SUCCESS, message=all_messages.BENEFICIARY_CREATE_SUCCESS, error=[], data={"beneficiary_id":details.id},code="")
            else:
                db.rollback()
                return Utility.json_response(status=INTERNAL_ERROR, message=all_messages.SOMTHING_WRONG, error=[], data={})
       
        else:
            db.rollback()
            return Utility.json_response(status=INTERNAL_ERROR, message=all_messages.SOMTHING_WRONG, error=[], data={})
       
    except Exception as E:
        print(E)
        db.rollback()
        return Utility.json_response(status=INTERNAL_ERROR, message=all_messages.SOMTHING_WRONG, error=[], data={})

@router.post("/update-benficiary", response_description="Update Benficiary")
async def update_benficiary(request: BeneficiaryEdit,background_tasks: BackgroundTasks,auth_user=Depends(AuthHandler().auth_wrapper), db: Session = Depends(get_database_session)):
    try:
        beneficiary_id = request.beneficiary_id
        user_id = auth_user["id"]
        full_name = request.full_name
        country_id = request.country_id
        city = request.city
        state_province = request.state_province
        postal_code = request.postal_code
        swift_code = request.swift_code
        iban = request.iban
        bank_name = request.bank_name
        bank_country_id = request.bank_country_id
        bank_address = request.bank_address
        
        user_obj = db.query(UserModel).filter(UserModel.id == user_id).first()
        if user_obj is None:            
            return Utility.json_response(status=500, message=all_messages.USER_NOT_EXISTS, error=[], data={},code="LOGOUT_ACCOUNT")            
        elif user_obj.role_id !=2:            
            return Utility.json_response(status=500, message=all_messages.NO_PERMISSIONS, error=[], data={},code="LOGOUT_ACCOUNT")            
        elif user_obj.status_id == 2:
            return Utility.json_response(status=500, message=all_messages.PENDING_EMAIL_VERIFICATION, error=[], data={},code="LOGOUT_ACCOUNT")            
        elif user_obj.status_id == 4:
            return Utility.json_response(status=500, message=all_messages.PROFILE_INACTIVE, error=[], data={},code="LOGOUT_ACCOUNT")            
        elif user_obj.status_id == 5:
            return Utility.json_response(status=500, message=all_messages.PROFILE_DELETED, error=[], data={},code="LOGOUT_ACCOUNT")
        
        exists_ben = db.query(BeneficiaryModel).filter(BeneficiaryModel.id == beneficiary_id,BeneficiaryModel.user_id==user_id).first()
        if exists_ben is None:
            return Utility.json_response(status=BUSINESS_LOGIG_ERROR, message=all_messages.BENEFICIARY_NOT_EXISTS, error=[], data={},code="BENEFICIARY_NOT_EXISTS")

        beneficiary = db.query(BeneficiaryModel).filter(BeneficiaryModel.id != beneficiary_id , BeneficiaryModel.iban == iban,BeneficiaryModel.user_id==user_id).first()
        if beneficiary is not None:
            return Utility.json_response(status=BUSINESS_LOGIG_ERROR, message=all_messages.BENEFICIARY_ALREADY_EXISTS, error=[], data={},code="BENEFICIARY_ALREADY_EXISTS")
        otp =Utility.generate_otp()
        exists_ben.full_name =full_name
        exists_ben.city=city
        exists_ben.country_id=country_id
        exists_ben.state_province=state_province
        exists_ben.postal_code=postal_code
        exists_ben.swift_code=swift_code
        exists_ben.iban=iban
        exists_ben.bank_name=bank_name
        exists_ben.bank_country_id=bank_country_id
        exists_ben.bank_address=bank_address
        exists_ben.status_id = 1
        otpdata = { "ref_id":exists_ben.id,"catrgory":"BeneficiaryModel","otp":otp,"user_id":user_id,"token":'' }
        otpdata["token"] = AuthHandler().encode_token(otpdata,minutes=6)        
        token_data = tokensModel(ref_id=exists_ben.id,token=otpdata["token"],catrgory="BeneficiaryModel", user_id=user_id,otp=otp,active=True)
        db.add(token_data)
        db.commit()
        if token_data.id:
            mail_data = {"otp":str(otp),"name":user_obj.first_name +" "+user_obj.last_name,"beneficiary_name":exists_ben.full_name}
            background_tasks.add_task(Email.send_mail,recipient_email=[user_obj.email], subject=all_messages.BENEFICIARY_UPDATED_SUCCESS, template='beneficiary_beneficiary_update.html',data=mail_data )
            return Utility.json_response(status=SUCCESS, message=all_messages.BENEFICIARY_UPDATED_SUCCESS, error=[], data={"beneficiary_id":exists_ben.id},code="")
        else:
            db.rollback()
            return Utility.json_response(status=INTERNAL_ERROR, message=all_messages.SOMTHING_WRONG, error=[], data={})
    

    except Exception as E:
        print(E)
        db.rollback()
        return Utility.json_response(status=INTERNAL_ERROR, message=all_messages.SOMTHING_WRONG, error=[], data={})

@router.post("/benficiary-list", response_model=PaginatedBeneficiaryResponse, response_description="Fetch Benficiary List")
async def get_benficiary_list(filter_data: BeneficiaryListReq,auth_user=Depends(AuthHandler().auth_wrapper),db: Session = Depends(get_database_session)):
    user_id = auth_user["id"]
    user_obj = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user_obj is None:            
            return Utility.json_response(status=500, message=all_messages.USER_NOT_EXISTS, error=[], data={},code="LOGOUT_ACCOUNT")            
    elif user_obj.role_id !=2:            
        return Utility.json_response(status=500, message=all_messages.NO_PERMISSIONS, error=[], data={},code="LOGOUT_ACCOUNT")            
    elif user_obj.status_id == 2:
        return Utility.json_response(status=500, message=all_messages.PENDING_EMAIL_VERIFICATION, error=[], data={},code="LOGOUT_ACCOUNT")            
    elif user_obj.status_id == 4:
        return Utility.json_response(status=500, message=all_messages.PROFILE_INACTIVE, error=[], data={},code="LOGOUT_ACCOUNT")            
    elif user_obj.status_id == 5:
        return Utility.json_response(status=500, message=all_messages.PROFILE_DELETED, error=[], data={},code="LOGOUT_ACCOUNT")
        
    if auth_user.get("role_id", -1) not in [2]:
        return Utility.json_response(status=BUSINESS_LOGIG_ERROR, message=all_messages.NO_PERMISSIONS, error=[], data={},code="NO_PERMISSIONS")

    
    query = db.query(BeneficiaryModel).options(
        joinedload(BeneficiaryModel.status_details),
        joinedload(BeneficiaryModel.beneficiary_country_details),
        joinedload(BeneficiaryModel.beneficiary_country_details),
        
    )
    query = query.filter(BeneficiaryModel.user_id==user_id)

    if filter_data.search_string:
        search = f"%{filter_data.search_string}%"
        query = query.filter(
            or_(
                BeneficiaryModel.full_name.ilike(search),
                BeneficiaryModel.short_name.ilike(search),
                BeneficiaryModel.email.ilike(search),
                BeneficiaryModel.mobile_no.ilike(search),
                BeneficiaryModel.city.ilike(search),
                BeneficiaryModel.state_province.ilike(search),
                BeneficiaryModel.postal_code.ilike(search),
                BeneficiaryModel.swift_code.ilike(search),
                BeneficiaryModel.iban.ilike(search),
                BeneficiaryModel.bank_name.ilike(search),
            )
        )
    if filter_data.status_ids:
        query = query.filter(BeneficiaryModel.status_id.in_(filter_data.status_ids))
    if filter_data.country_ids:
        query = query.filter(BeneficiaryModel.country_id.in_(filter_data.country_ids))
    if filter_data.bank_country_ids:
        query = query.filter(BeneficiaryModel.bank_country_id.in_(filter_data.bank_country_ids))
        
    
     # Total count of users matching the filters
    total_count = query.count()
    sort_column = getattr(BeneficiaryModel, filter_data.sort_by, None)
    if sort_column:
        if filter_data.sort_order == "desc":
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc("created_on"))

    # Apply pagination
    offset = (filter_data.page - 1) * filter_data.per_page
    paginated_query = query.offset(offset).limit(filter_data.per_page).all()
    # Create a paginated response
    return PaginatedBeneficiaryResponse(
        total_count=total_count,
        list=paginated_query,
        page=filter_data.page,
        per_page=filter_data.per_page
    )

@router.post("/get-beneficiary",response_description="Get Beneficiary Details")
async def get_benficiary( request: GetBeneficiaryDetails,background_tasks: BackgroundTasks,auth_user=Depends(AuthHandler().auth_wrapper), db: Session = Depends(get_database_session)):
    try:
        beneficiary_id = request.beneficiary_id
        user_id = auth_user["id"]
        user_obj = db.query(UserModel).filter(UserModel.id == user_id).first()
        if user_obj is None:            
            return Utility.json_response(status=500, message=all_messages.USER_NOT_EXISTS, error=[], data={},code="LOGOUT_ACCOUNT")            
        elif user_obj.role_id !=2:            
            return Utility.json_response(status=500, message=all_messages.NO_PERMISSIONS, error=[], data={},code="LOGOUT_ACCOUNT")            
        elif user_obj.status_id == 2:
            return Utility.json_response(status=500, message=all_messages.PENDING_EMAIL_VERIFICATION, error=[], data={},code="LOGOUT_ACCOUNT")            
        elif user_obj.status_id == 4:
            return Utility.json_response(status=500, message=all_messages.PROFILE_INACTIVE, error=[], data={},code="LOGOUT_ACCOUNT")            
        elif user_obj.status_id == 5:
            return Utility.json_response(status=500, message=all_messages.PROFILE_DELETED, error=[], data={},code="LOGOUT_ACCOUNT")
         
        exists_ben = db.query(BeneficiaryModel).filter(BeneficiaryModel.id == beneficiary_id,BeneficiaryModel.user_id==user_id).first()
        if exists_ben is None:            
            return Utility.json_response(status=BUSINESS_LOGIG_ERROR, message=all_messages.BENEFICIARY_NOT_EXISTS, error=[], data={},code="BENEFICIARY_NOT_EXISTS")
        else:
            response_data = Utility.model_to_dict(exists_ben)
            response_data["beneficiary_id"] = response_data["id"]
            response_data["beneficiary_country_details"] = Utility.model_to_dict(exists_ben.beneficiary_country_details)
            response_data["beneficiary_bank_country_details"] = Utility.model_to_dict(exists_ben.beneficiary_bank_country_details)
            response_data["status_details"] = Utility.model_to_dict(exists_ben.status_details)
            return Utility.json_response(status=SUCCESS, message="Beneficiary Details", error=[], data=response_data,code="")

    except Exception as E:
        print(E)
        db.rollback()
        return Utility.json_response(status=INTERNAL_ERROR, message=all_messages.SOMTHING_WRONG, error=[], data={})

@router.post("/activate-benficiary", response_description="Activate Benficiary ")
async def activate_benficiary_status(request: ActivateBeneficiary,background_tasks: BackgroundTasks,auth_user=Depends(AuthHandler().auth_wrapper), db: Session = Depends(get_database_session)):
    try:
        beneficiary_id = request.beneficiary_id
        user_id = auth_user["id"]
        otp = request.otp
        
        user_obj = db.query(UserModel).filter(UserModel.id == user_id).first()
        if user_obj is None:            
            return Utility.json_response(status=500, message=all_messages.USER_NOT_EXISTS, error=[], data={},code="LOGOUT_ACCOUNT")            
        elif user_obj.role_id !=2:            
            return Utility.json_response(status=500, message=all_messages.NO_PERMISSIONS, error=[], data={},code="LOGOUT_ACCOUNT")            
        elif user_obj.status_id == 2:
            return Utility.json_response(status=500, message=all_messages.PENDING_EMAIL_VERIFICATION, error=[], data={},code="LOGOUT_ACCOUNT")            
        elif user_obj.status_id == 4:
            return Utility.json_response(status=500, message=all_messages.PROFILE_INACTIVE, error=[], data={},code="LOGOUT_ACCOUNT")            
        elif user_obj.status_id == 5:
            return Utility.json_response(status=500, message=all_messages.PROFILE_DELETED, error=[], data={},code="LOGOUT_ACCOUNT")
         
        exists_ben = db.query(BeneficiaryModel).filter(BeneficiaryModel.id == beneficiary_id,BeneficiaryModel.user_id==user_id).first()
        if exists_ben is None:
            return Utility.json_response(status=BUSINESS_LOGIG_ERROR, message=all_messages.BENEFICIARY_NOT_EXISTS, error=[], data={},code="BENEFICIARY_NOT_EXISTS")
        
        
        token_query = db.query(tokensModel).filter(tokensModel.catrgory =="BeneficiaryModel", tokensModel.user_id==user_id, tokensModel.otp == otp,tokensModel.active==True).first()
        if token_query is None:
            return Utility.json_response(status=BUSINESS_LOGIG_ERROR, message=all_messages.INVALIED_OTP, error=[], data={},code="")
        else:
            token_data = AuthHandler().decode_otp_token(token_query.token)
            
            if str(token_data["otp"]) == str(otp):
                exists_ben.status_id = 2
                token_query.active = False
                db.commit()
                status_msg = "Activated"
                msg = f"Beneficiary {status_msg} successfully"
                return Utility.json_response(status=SUCCESS, message=msg, error=[], data={"beneficiary_id":exists_ben.id},code="")
            else:
                
                return Utility.json_response(status=BUSINESS_LOGIG_ERROR, message=all_messages.INVALIED_OTP, error=[], data={},code="")
        
    except Exception as E:
        print(E)
        db.rollback()
        return Utility.json_response(status=INTERNAL_ERROR, message=all_messages.SOMTHING_WRONG, error=[], data={})

@router.post("/update-benficiary-status", response_description="Update Benficiary Status")
async def update_benficiary_status(request: UpdateBeneficiaryStatus,background_tasks: BackgroundTasks,auth_user=Depends(AuthHandler().auth_wrapper), db: Session = Depends(get_database_session)):
    try:
        beneficiary_id = request.beneficiary_id
        user_id = auth_user["id"]
        status_id = request.status_id
        #otp = request.otp
        if status_id<=2:
            return Utility.json_response(status=BUSINESS_LOGIG_ERROR, message=all_messages.INVALID_SATUS_SELECTED, error=[], data={},code="INVALID_SATUS_SELECTED")
        
        user_obj = db.query(UserModel).filter(UserModel.id == user_id).first()
        if user_obj is None:            
            return Utility.json_response(status=500, message=all_messages.USER_NOT_EXISTS, error=[], data={},code="LOGOUT_ACCOUNT")            
        elif user_obj.role_id !=2:            
            return Utility.json_response(status=500, message=all_messages.NO_PERMISSIONS, error=[], data={},code="LOGOUT_ACCOUNT")            
        elif user_obj.status_id == 2:
            return Utility.json_response(status=500, message=all_messages.PENDING_EMAIL_VERIFICATION, error=[], data={},code="LOGOUT_ACCOUNT")            
        elif user_obj.status_id == 4:
            return Utility.json_response(status=500, message=all_messages.PROFILE_INACTIVE, error=[], data={},code="LOGOUT_ACCOUNT")            
        elif user_obj.status_id == 5:
            return Utility.json_response(status=500, message=all_messages.PROFILE_DELETED, error=[], data={},code="LOGOUT_ACCOUNT")
         
        exists_ben = db.query(BeneficiaryModel).filter(BeneficiaryModel.id == beneficiary_id,BeneficiaryModel.user_id==user_id).first()
        if exists_ben is None:
            return Utility.json_response(status=BUSINESS_LOGIG_ERROR, message=all_messages.BENEFICIARY_NOT_EXISTS, error=[], data={},code="BENEFICIARY_NOT_EXISTS")
        
        if exists_ben.status_id == status_id:
            return Utility.json_response(status=BUSINESS_LOGIG_ERROR, message=all_messages.BENEFICIARY_IS_SAME_STATUS, error=[], data={},code="BENEFICIARY_IS_SAME_STATUS")
        
        # token_query = db.query(tokensModel).filter(tokensModel.catrgory =="BeneficiaryModel", tokensModel.user_id==user_id, tokensModel.otp == otp,tokensModel.active==True).first()
        # if token_query is None:
        #     return Utility.json_response(status=BUSINESS_LOGIG_ERROR, message=all_messages.INVALIED_OTP, error=[], data={},code="")
        
        exists_ben.status_id = status_id
        #token_query.active = False
        db.commit()
        status_msg = "updated"
        if status_id==2:
            status_msg ="Activated"
        if status_id==3:
            status_msg ="In-activated"


        msg = f"Beneficiary {status_msg} successfully"
        return Utility.json_response(status=SUCCESS, message=msg, error=[], data={"beneficiary_id":exists_ben.id},code="")
    
    except Exception as E:
        print(E)
        db.rollback()
        return Utility.json_response(status=INTERNAL_ERROR, message=all_messages.SOMTHING_WRONG, error=[], data={})


@router.post("/resend-benficiary-otp", response_description="Generate new otp")
async def send_benficiary_otp(request: ResendBeneficiaryOtp,background_tasks: BackgroundTasks,auth_user=Depends(AuthHandler().auth_wrapper), db: Session = Depends(get_database_session)):
    try:
        beneficiary_id = request.beneficiary_id
        user_id = auth_user["id"]
        user_obj = db.query(UserModel).filter(UserModel.id == user_id).first()
        if user_obj is None:            
            return Utility.json_response(status=500, message=all_messages.USER_NOT_EXISTS, error=[], data={},code="LOGOUT_ACCOUNT")            
        elif user_obj.role_id !=2:            
            return Utility.json_response(status=500, message=all_messages.NO_PERMISSIONS, error=[], data={},code="LOGOUT_ACCOUNT")            
        elif user_obj.status_id == 2:
            return Utility.json_response(status=500, message=all_messages.PENDING_EMAIL_VERIFICATION, error=[], data={},code="LOGOUT_ACCOUNT")            
        elif user_obj.status_id == 4:
            return Utility.json_response(status=500, message=all_messages.PROFILE_INACTIVE, error=[], data={},code="LOGOUT_ACCOUNT")            
        elif user_obj.status_id == 5:
            return Utility.json_response(status=500, message=all_messages.PROFILE_DELETED, error=[], data={},code="LOGOUT_ACCOUNT")
         
        otp =Utility.generate_otp()
        mail_data = {"otp":str(otp),"name":user_obj.first_name +" "+user_obj.last_name}
        background_tasks.add_task(Email.send_mail,recipient_email=[user_obj.email], subject=all_messages.PENDING_EMAIL_VERIFICATION_OTP_SUBJ, template='beneficiary_verification_otp.html',data=mail_data )
        otpdata = { "ref_id":beneficiary_id,"catrgory":"BeneficiaryModel","otp":otp,"user_id":user_id,"token":'' }
        otpdata["token"] = AuthHandler().encode_token(otpdata,minutes=6)
        token_data = tokensModel(ref_id=beneficiary_id,token=otpdata["token"],catrgory="BeneficiaryModel",user_id=user_id,otp=otp)
        db.add(token_data)
        db.commit()
        if token_data.id:
            return Utility.json_response(status=SUCCESS, message=all_messages.RESEND_VERIFICATION_OTP, error=[], data={"beneficiary_id":beneficiary_id},code="")
        else:
            db.rollback()
            return Utility.json_response(status=INTERNAL_ERROR, message=all_messages.SOMTHING_WRONG, error=[], data={})
    
        
    except Exception as E:
        print(E)
        db.rollback()
=======
@router.post("/list", response_description="Fetch Users List")
async def get_users_list(request: UsersList, db: Session = Depends(get_database_session)):
    try:
        # Base query
        query = select(UserModel.id,UserModel.first_name,UserModel.last_name, UserModel.status_id,UserModel.country_id,UserModel.email,MdCountries.name).join(MdCountries, UserModel.country_id == MdCountries.id ,)
        
        # Apply filters
        filters = []
        if request.search_text:
            filters.append(UserModel.email.ilike(f"%{request.search_text}%"))
        
        # Example filter usage
        if request.filters:
            for key, value in request.filters.items():
                if hasattr(UserModel, key):
                    column = getattr(UserModel, key)
                    if isinstance(column.type, Integer):
                        filters.append(column == int(value))
                    elif isinstance(column.type, String):
                        filters.append(column.ilike(f"%{value}%"))
                    elif isinstance(column.type, Date) and isinstance(value, str):
                        filters.append(column == datetime.strptime(value, '%Y-%m-%d').date())
                    elif isinstance(column.type, DateTime) and isinstance(value, str):
                        filters.append(column == datetime.strptime(value, '%Y-%m-%dT%H:%M:%S'))

        # if filters:
        #     query = query.where(and_(*filters))

        # Calculate pagination parameters
        page = request.page
        per_page = request.per_page
        offset = (page - 1) * per_page

        # Apply pagination
        query_with_pagination = query.offset(offset).limit(per_page)

        # Fetch users
        with db.execute(query_with_pagination) as result:
            rows = result.fetchall()
            #users_list = [dict(row._asdict()) for row in rows]
            users_list = [dict(row._mapping) for row in rows]
            #users_list = [Utility.model_to_dict(row) for row in rows]
            #users_list = [serialize_model(row) for row in rows]
            
            

            

        # Get total count
        count_query = select(func.count()).select_from(UserModel).where(and_(*filters)) if filters else select(func.count()).select_from(UserModel)
        with db.execute(count_query) as result:
            total_count = result.scalar()
            print(total_count)

        # Prepare response data
        res_data = {
            "list": users_list,
            "page": page,
            "per_page": per_page,
            "total_count": total_count
        }
        
        return Utility.json_response(status=SUCCESS, message=all_messages.UPDATE_PASSWORD_SUCCESS, error=[], data=res_data,code="")
            

    except Exception as e:
        print(e)  # For debugging purposes
        # Ensure to handle rollback correctly
>>>>>>> 4ff072eea4bf3d9e21bdfa50534e18dd866d673d
        return Utility.json_response(status=INTERNAL_ERROR, message=all_messages.SOMTHING_WRONG, error=[], data={})

