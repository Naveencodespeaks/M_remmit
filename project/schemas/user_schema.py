from pydantic import BaseModel, EmailStr, Field, ValidationError, validator,field_validator
import phonenumbers
from phonenumbers import NumberParseException, is_valid_number
import re
<<<<<<< HEAD
from datetime import date, datetime, timedelta
from typing import Optional, List
=======
from datetime import date, datetime
from typing import Optional
>>>>>>> 4ff072eea4bf3d9e21bdfa50534e18dd866d673d




class UpdateProfile(BaseModel):    
    
    first_name: str
    last_name: str
    date_of_birth: date = Field(..., description="Must be at least 18 years old.And format should be YYYY-MM-DD")
    mobile_no: str = Field(..., description="The mobile phone number of the user, including the country code.")
   
    @field_validator('date_of_birth', mode='before')
    def validate_date_of_birth(cls, v, info):
        # Ensure v is a date object
        if isinstance(v, str):
            v = date.fromisoformat(v)  # Convert from string to date if needed
        today = date.today()
        age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))
        if age < 18:
            raise ValueError('You must be at least 18 years old. And format should be YYYY-MM-DD')
        return v

    
    @field_validator('first_name', mode='before')
    def validate_first_name(cls, v, info):
        v = v.strip()
        if not re.match(r'^[A-Za-z]+$', v):
            raise ValueError('First name must only contain alphabetic characters and cannot include numbers, special characters, or spaces.')
        return v
    
    @field_validator('last_name', mode='before')
    def validate_last_name(cls, v, info):
        v = v.strip()
        if not re.match(r'^[A-Za-z]+$', v):
            raise ValueError('Last name must only contain alphabetic characters and cannot include numbers, special characters, or spaces.')
        return v

    @field_validator('mobile_no', mode='before')
    def validate_mobile_no(cls, v, info):
        try:
            phone_number = phonenumbers.parse(v)
            if not is_valid_number(phone_number):
                raise ValueError('Invalid phone number.')
        except NumberParseException:
            raise ValueError('Invalid phone number format.')
        return v
    
   

<<<<<<< HEAD
class UpdatePassword(BaseModel):
=======
class UpdatePassword(BaseModel):    
>>>>>>> 4ff072eea4bf3d9e21bdfa50534e18dd866d673d
    old_password:str
    password: str
    confirm_password: str = Field(..., description="Test Search")
    
    @field_validator('password', 'confirm_password', mode='before')
    def passwords_match(cls, v, info):
        v = v.strip()
        # Access other values from info.
        if info.field_name == 'confirm_password':
            password = info.data.get('password')
            if v != password:
                raise ValueError('Password and Confirm Password do not match.')
        return v
    
    @field_validator('password', 'old_password', mode='before')
    def password(cls, v, info):
        v = v.strip()
        # Access other values from info.
        if info.field_name == 'old_password':
            password = info.data.get('password')
            if v == password:
                raise ValueError('New Password Should not same with Old Password.')
        return v

<<<<<<< HEAD
    class Config:
        #orm_mode = True
        from_attributes = True
        str_strip_whitespace = True

class ListRequestBase(BaseModel):
    search_string: Optional[str] = None  # Search string on string based columns
    page:int = 1
    per_page:int =25
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    sort_by: Optional[str] = "created_on"  # Default sort by 'created_on'
    sort_order: Optional[str] = "desc"

    @field_validator('start_date', )
    def start_date_convert_datetime_to_date(cls, v):
        if isinstance(v, datetime):
           return (v - timedelta(days=1)).date()
        elif isinstance(v, date):
           return (v - timedelta(days=1))
        else:
            return v   
        
    @field_validator( 'end_date' )
    def end_date_convert_datetime_to_date(cls, v):
        
        if isinstance(v, datetime):           
           return (v + timedelta(days=1)).date()
        elif isinstance(v, date):           
           return (v + timedelta(days=1))
        else:
            return v   
           
        
        
class UserFilterRequest(ListRequestBase):
    
    tenant_id: Optional[List[int]] = None
    #role_id: Optional[List[int]] = None
    status_ids: Optional[List[int]] = None  # List of status IDs
    country_id: Optional[List[int]] = None
    #state_id: Optional[List[int]] = None
    #location_id: Optional[List[int]] = None
    kyc_status_id: Optional[List[int]] = None
    #accepted_terms: Optional[bool] = None

    

class BeneficiaryListReq(ListRequestBase):
    
    status_ids: Optional[List[int]] = None
    country_ids: Optional[List[int]] = None
    bank_country_ids:Optional[List[int]] = None
    
    
=======

class UsersList(BaseModel):
    page: int = Field(default=1, gt=0, description="Current page number, must be greater than 0")
    per_page: int = Field(default=10, gt=0, description="Number of users per page, must be greater than 0")
    search_text:Optional[str] = None
    filters:Optional[dict] ={}
    

>>>>>>> 4ff072eea4bf3d9e21bdfa50534e18dd866d673d

class CountryResponse(BaseModel):
    id: int
    name: str

    class Config:
<<<<<<< HEAD
        #orm_mode = True
        from_attributes = True
        str_strip_whitespace = True

class MasterDataResponse(BaseModel):
    id: int
    name: str

    class Config:
        #orm_mode = True
        from_attributes = True
        str_strip_whitespace = True


class UserListResponse(BaseModel):
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: str
    mobile_no: Optional[str] = None
    tenant_id: Optional[int] = None
    role_id: int
    status_id: int
    country_id: Optional[int] = None
    state_id: Optional[int] = None
    location_id: Optional[int] = None
    kyc_status_id: int
    accepted_terms: bool
    tenant_details: Optional[MasterDataResponse] = None
    role_details: Optional[MasterDataResponse] = None
    status_details: Optional[MasterDataResponse] = None
    country_details: Optional[CountryResponse] = None
    #state_details: Optional[MasterDataResponse] = None
    #location_details: Optional[MasterDataResponse] = None
    kyc_status: Optional[MasterDataResponse] = None
    created_on:Optional[date]
    updated_on:Optional[date]
    #6787425996

    @field_validator('created_on', 'updated_on', mode='before' )
    def convert_datetime_to_date(cls, v):
        if isinstance(v, datetime):
            return v.date()
        return v
    class Config:
        #orm_mode = True
        from_attributes = True
        str_strip_whitespace = True
class PaginatedUserResponse(BaseModel):
    total_count: int
    list: List[UserListResponse]
    page: int
    per_page: int
    
class GetUserDetailsReq(BaseModel):
    user_id:int
    class Config:
        from_attributes = True
        str_strip_whitespace = True

class UpdateUserDetails(BaseModel):
    street: str
    city: str
    state:str
    pincode: str
    occupation: str
    annual_income:int
    

class UpdateKycDetails(BaseModel):
    pass


class BeneficiaryRequest(BaseModel):
    
    #user_id: int
    full_name: str
    email:Optional[EmailStr]=''
    mobile_no: str = None
    #short_name: Optional[str] = ""
    country_id: int
    city: str
    state_province: str
    postal_code: str
    swift_code: str
    iban: str
    conform_iban: str
    bank_name: str
    bank_country_id: int
    bank_address: str

    @field_validator('full_name', mode='before')
    def validate_full_name(cls, v, info):
        v = v.strip()
        if v is None or v=='':
            raise ValueError('Full name required!')
        if not re.match(r'^[A-Za-z ]+$', v):
            raise ValueError('full name must only contain alphabetic characters and cannot include numbers, special characters, or spaces.')
        return v

    @field_validator('mobile_no', mode='before')
    def validate_mobile_no(cls, v, info):
        try:
            phone_number = phonenumbers.parse(v)
            if not is_valid_number(phone_number):
                raise ValueError('Invalid phone number.')
        except NumberParseException:
            raise ValueError('Invalid phone number format.')
        return v
    
    @field_validator('city', mode='before')
    def validate_city(cls, v, info):
        v = v.strip()
        if v is None or v=='':
            raise ValueError('City required!')
        return v
    
    @field_validator('state_province', mode='before')
    def validate_state_province(cls, v, info):
        v = v.strip()
        if v is None or v=='':
            raise ValueError('State/ Province required!')
        return v
    
    @field_validator('postal_code', mode='before')
    def validate_postal_code(cls, v, info):
        v = v.strip()
        if v is None or v=='':
            raise ValueError('postal_code required!')
        return v
     

    @field_validator('swift_code', mode='before')
    def validate_swift_code(cls, v, info):
        v = v.strip()
        min_length = 8
        max_length = 11

        if len(v) < min_length:
            raise ValueError(f'swift code must be at least {min_length} characters long.')
        if len(v) > max_length:
            raise ValueError(f'swift code must be at most {max_length} characters long.')
        return v
    

    @field_validator('iban',  mode='before')
    def iban_validate(cls, v, info):
        max_length = 50
        min_length = 5
        v = v.strip()
        if v is None or v=='':
            raise ValueError('iban is required!')
        if len(v) < min_length:
            raise ValueError(f'iban must be at least {min_length} characters long.')
        
        if len(v) > max_length:
            raise ValueError(f'iban must be at most {max_length} characters long.')
        
        return v
    
    @field_validator('iban', 'conform_iban', mode='before')
    def passwords_match(cls, v, info):
        v = v.strip()
        if v is None or v=='':
            raise ValueError('iban is required!')
        
        elif info.field_name == 'confirm_password':
            iban = info.data.get('iban')
            if v != iban:
                raise ValueError('iban and Confirm iban do not match.')
        return v

    
    @field_validator('bank_name', mode='before')
    def validate_bank_name(cls, v, info):
        v = v.strip()
        if v is None or v=='':
            raise ValueError('Bank  Name required!')
        return v
    
    @field_validator('bank_address', mode='before')
    def validate_bank_address(cls, v, info):
        v = v.strip()
        if v is None or v=='':
            raise ValueError('Bank  Address required!')
        return v
    
    
    
         
    

    
    
    class Config:
        from_attributes = True
        str_strip_whitespace = True

class BeneficiaryEdit(BaseModel):
    beneficiary_id:int
    full_name: str
    email:Optional[EmailStr] =""
    mobile_no: str = None
    country_id: int
    city: str
    state_province: str
    postal_code: str
    swift_code: str
    iban: str
    conform_iban: str
    bank_name: str
    bank_country_id: int
    bank_address: str

    @field_validator('full_name', mode='before')
    def validate_full_name(cls, v, info):
        v = v.strip()
        if v is None or v=='':
            raise ValueError('Full name required!')
        if not re.match(r'^[A-Za-z ]+$', v):
            raise ValueError('full name must only contain alphabetic characters and cannot include numbers, special characters, or spaces.')
        return v

    @field_validator('mobile_no', mode='before')
    def validate_mobile_no(cls, v, info):
        try:
            phone_number = phonenumbers.parse(v)
            if not is_valid_number(phone_number):
                raise ValueError('Invalid phone number.')
        except NumberParseException:
            raise ValueError('Invalid phone number format.')
        return v
    
    @field_validator('city', mode='before')
    def validate_city(cls, v, info):
        v = v.strip()
        if v is None or v=='':
            raise ValueError('City required!')
        return v
    
    @field_validator('state_province', mode='before')
    def validate_state_province(cls, v, info):
        v = v.strip()
        if v is None or v=='':
            raise ValueError('State / Province required!')
        return v
    
    @field_validator('postal_code', mode='before')
    def validate_postal_code(cls, v, info):
        v = v.strip()
        if v is None or v=='':
            raise ValueError('Postal code required!')
        return v
     

    @field_validator('swift_code', mode='before')
    def validate_swift_code(cls, v, info):
        v = v.strip()
        min_length = 8
        max_length = 11

        if len(v) < min_length:
            raise ValueError(f'swift code must be at least {min_length} characters long.')
        if len(v) > max_length:
            raise ValueError(f'swift code must be at most {max_length} characters long.')
        return v
    

    @field_validator('iban',  mode='before')
    def iban_validate(cls, v, info):
        max_length = 50
        min_length = 5
        v = v.strip()
        if v is None or v=='':
            raise ValueError('iban is required!')
        if len(v) < min_length:
            raise ValueError(f'iban must be at least {min_length} characters long.')
        
        if len(v) > max_length:
            raise ValueError(f'iban must be at most {max_length} characters long.')
        
        return v
    
    @field_validator('iban', 'conform_iban', mode='before')
    def passwords_match(cls, v, info):
        v = v.strip()
        if v is None or v=='':
            raise ValueError('iban is required!')
        
        elif info.field_name == 'conform_iban':
            password = info.data.get('iban')
            if v != password:
                raise ValueError('iban and Confirm iban do not match.')
        return v

    
    @field_validator('bank_name', mode='before')
    def validate_bank_name(cls, v, info):
        v = v.strip()
        if v is None or v=='':
            raise ValueError('Bank  Name required!')
        return v
    
    @field_validator('bank_address', mode='before')
    def validate_bank_address(cls, v, info):
        v = v.strip()
        if v is None or v=='':
            raise ValueError('Bank  Address required!')
        return v
    
    class Config:
        from_attributes = True
        str_strip_whitespace = True
class GetBeneficiaryDetails(BaseModel):
    beneficiary_id:int
    class Config:
        from_attributes = True
        str_strip_whitespace = True

class UpdateBeneficiaryStatus(BaseModel):
    beneficiary_id:int
    #otp:str
    status_id:int
    class Config:
        from_attributes = True
        str_strip_whitespace = True
class ActivateBeneficiary(BaseModel):
    beneficiary_id:int
    otp:str
    
    class Config:
        from_attributes = True
        str_strip_whitespace = True



class ResendBeneficiaryOtp(BaseModel):
    beneficiary_id:int



class BeneficiaryResponse(BaseModel):
    id: int
    user_id: int
    full_name: Optional[str] = None
    short_name: Optional[str] = ""
    email:str=""
    mobile_no: str = ''
    country_id: int
    beneficiary_country_details: Optional[CountryResponse] = None
    city: Optional[str] = None
    state_province: Optional[str] = None
    postal_code: Optional[str] = None
    swift_code: Optional[str] = None
    iban: Optional[str] = None
    bank_name: Optional[str] = None
    bank_country_id: int
    beneficiary_bank_country_details:Optional[CountryResponse] = None
    bank_address: Optional[str] = None

    class Config:
        from_attributes = True
        str_strip_whitespace = True

class PaginatedBeneficiaryResponse(BaseModel):
    total_count: int
    list: List[BeneficiaryResponse]
    page: int
    per_page: int
   
=======
        orm_mode = True
        from_attributes=True

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    status_id: int
    country: CountryResponse  # Use the Pydantic model for related details

    class Config:
        orm_mode = True
        from_attributes=True
>>>>>>> 4ff072eea4bf3d9e21bdfa50534e18dd866d673d
