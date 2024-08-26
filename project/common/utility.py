from fastapi.responses import JSONResponse
import uuid
import random
from datetime import datetime


class Utility:
    @staticmethod
    def json_response(status, message, error, data,code=''):
        return JSONResponse({
            'status': status,
            'message': message,
            'error': error,
            'result': data,
            "code": code if code else''
        })

    @staticmethod
    def dict_response(status, message, error, data,code=''):
        return ({
            'status': status,
            'message': message,
            'error': error,
            'result': data,
            "code": code if code else''
        })
    @staticmethod
    def generate_otp(n: int=6) -> int:
        range_start = 10**(n-1)
        range_end = (10**n) - 1
        otp = random.randint(range_start, range_end)
        return otp

    @staticmethod
    def uuid():
        return str(uuid.uuid4())


    @staticmethod
    def model_to_dict(model_instance):
        
        if model_instance is None:
            return {}
    
        result = {}
        for column in model_instance.__table__.columns:
            if column.name !="created_on" and column.name !="updated_on" and column.name !="date_of_birth" :
                value = getattr(model_instance, column.name)
                if isinstance(value, datetime):
                    result[column.name] = value.isoformat()  # Convert datetime to ISO 8601 string
                else:
                    result[column.name] = value
        return result

    @staticmethod
    def convert_dtring_to_date(string_date=''):
        result =""
        if string_date is None:
            return result
        date_format = "%Y-%m-%d" # format YYYY-DD-MM
        datetime_obj = datetime.strptime(string_date, date_format)
        result = datetime_obj.date()
    
        
        
        return result

#print(Utility.uuid())
