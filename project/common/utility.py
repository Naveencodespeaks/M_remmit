from fastapi.responses import JSONResponse
import uuid
import random
from datetime import datetime,date
from sqlalchemy import desc, asc
from typing import List, Tuple


class Utility:
    @staticmethod
    def json_response(status, message, error, data,code=''):
        return JSONResponse({
            'status': status,
            'message': message,
            'error': error,
            'result': data,
            "code": code if code else''
        },status_code=status if status else 500)

    @staticmethod
    def dict_response(status, message, error, data,code=''):
        return ({
            'status': status,
            'message': message,
            'error': error,
            'result': data,
            "code": code if code else'',
            "status_code":status if status else 500
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
            value = getattr(model_instance, column.name)
            # if column.name !="created_on" and column.name !="updated_on" and column.name !="date_of_birth" :
            #     
            #     if isinstance(value, datetime):
            #         result[column.name] = value.isoformat()  # Convert datetime to ISO 8601 string
            #     else:
            #         result[column.name] = value
            if isinstance(value, datetime):
                result[column.name] =value.isoformat()
            elif isinstance(value, date):
                result[column.name] =value.isoformat()
            
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

    @staticmethod
    def list_query(Session=None,page=1,par_page=25,sort_by="id",sort_order="asc",response_schema=None,modelRef=None,filters={}):

        def get_data(db: Session,page: int = page,per_page: int = par_page,sort_by: str = sort_by,sort_order: str = sort_order,filters={}) -> Tuple[List[response_schema], int]:
            sort_column = desc(sort_by) if sort_order == "desc" else asc(sort_by)
            # Calculate offset and limit
            offset = (page - 1) * per_page
            filters = []
            if filters.search_text:
                filters.append(modelRef.email.ilike(f"%{filters.search_text}%"))
            
            query = db.query(modelRef)
            for key, value in filters.items():
                query = query.filter(getattr(modelRef, key) == value)

            total_count = db.query(modelRef).count()
            results = query.order_by(sort_column).offset(offset).limit(per_page).all()
            list = [response_schema.from_orm(result) for result in results]
            return total_count, list
        
        return get_data(Session=Session,page=page,par_page=par_page,sort_by=sort_by,sort_order=sort_order,response_schema=response_schema,modelRef=modelRef,filters=filters)



#print(Utility.uuid())
