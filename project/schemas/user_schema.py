from pydantic import BaseModel, EmailStr, Field, ValidationError, validator,field_validator
import phonenumbers
from phonenumbers import NumberParseException, is_valid_number
import re
from datetime import date, datetime
from typing import Optional




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
    
   

class UpdatePassword(BaseModel):    
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


class UsersList(BaseModel):
    page: int = Field(default=1, gt=0, description="Current page number, must be greater than 0")
    per_page: int = Field(default=10, gt=0, description="Number of users per page, must be greater than 0")
    search_text:Optional[str] = None
    filters:Optional[dict] ={}
    


class CountryResponse(BaseModel):
    id: int
    name: str

    class Config:
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