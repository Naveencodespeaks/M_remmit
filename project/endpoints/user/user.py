from datetime import datetime, timezone,timedelta
from datetime import datetime
from ...models.user_model import UserModel
from ...models.master_data_models import MdUserRole,MdUserStatus,MdCountries

from . import APIRouter, Utility, SUCCESS, FAIL, EXCEPTION ,INTERNAL_ERROR,BAD_REQUEST,BUSINESS_LOGIG_ERROR, Depends, Session, get_database_session, AuthHandler
from ...schemas.user_schema import UpdatePassword,UsersList,UserResponse,UpdateProfile
import re
from ...constant import messages as all_messages
from ...common.mail import Email
from sqlalchemy.sql import select, and_, or_, not_,func
from sqlalchemy.future import select
from datetime import date, datetime
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey, func
from sqlalchemy.ext.asyncio import AsyncSession


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

def serialize_model(instance):
    """Convert SQLAlchemy ORM model instance to dictionary."""
    return {column.name: getattr(instance, column.name) for column in instance.__table__.columns}

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
        return Utility.json_response(status=INTERNAL_ERROR, message=all_messages.SOMTHING_WRONG, error=[], data={})

