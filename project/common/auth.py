import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
import ast
import json
import jsonpickle
#from ..constant.status_constant import FAIL

class AuthHandler:
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = 'SECRET_REMMITANCE'

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        try:
            return self.pwd_context.verify(plain_password, hashed_password)
        except Exception as e:
            return False
    

    def datetime_handler(self,x):
        if isinstance(x, datetime):
            return x.isoformat()
        return x #TypeError("Type not serializable")
    
    def encode_token(self, user_dict):
        payload = {
        'exp': datetime.utcnow() + timedelta(minutes=60),
        'iat': datetime.utcnow(),
        'sub': jsonpickle.dumps(user_dict)  # Use jsonpickle to handle complex objects
       }
        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )
    
    
    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return json.loads(payload['sub'], )
            
        except jwt.ExpiredSignatureError:
            response = {}
            response.update(status=401, message="The time you were taken has expired!", error=[], data={},code="LOGIN_TOKEN_EXPIRED")
            raise HTTPException(status_code=401, detail=response)
        except jwt.InvalidTokenError as e:
            print(e)
            response = {}
            response.update(status=401, message="Invalied taken", error=[], data={},code="INVALIED_TOKEN")
            raise HTTPException(status_code=401, detail=response)

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)
