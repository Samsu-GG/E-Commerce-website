from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from App.config import security_settings
from uuid import uuid4
import jwt



def generate_access_token(
        data : dict,
        token_expire : timedelta = timedelta(days=1),
) -> str:
   jwt_token = jwt.encode(
            payload={
                **data,
                "jti" : str(uuid4()),
                "exp" : datetime.now(timezone.utc) + token_expire
            },
            algorithm= security_settings.JWT_ALGORITHM,
            key= security_settings.JWT_SECRET_KEY
        )
   return jwt_token

def decode_access_token(jwt_token : str) -> dict:
    try:
        jwt_decoded = jwt.decode(
            jwt=jwt_token,
            key=security_settings.JWT_SECRET_KEY,
            algorithms=[security_settings.JWT_ALGORITHM]
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401,detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401,detail="Invalid token")
    
    return jwt_decoded