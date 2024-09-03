from pydantic import BaseModel, EmailStr, Field, ValidationError, validator,field_validator
import re
from datetime import date, datetime


class TicketRequest(BaseModel):
    # id:int
    user_id:int
    description:str


    @field_validator('user_id', mode='before')
    def check_user_id(cls, v, info):
        if v is None or v<=0:
            raise ValueError('User ID is required and cannot be None.')
        return v
    
    @field_validator('description', mode='before')
    def check_description(cls, v):
        if v is None:
            raise ValueError('Description is required and cannot be None.')
        return v