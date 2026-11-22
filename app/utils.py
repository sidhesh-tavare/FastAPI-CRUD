from datetime import datetime,timezone,timedelta
from fastapi import HTTPException , status , Depends
from app.config import loginsettings 
from uuid import uuid4

import jwt

def generate_access_token(data : dict):
    return jwt.encode(
            payload={
                **data,
                "jti" : str(uuid4()),
                "exp": datetime.now(timezone.utc)
            },
            algorithm = loginsettings.algorithm,
            key = loginsettings.signature
        )

def decode_access_token(token: str) -> dict:

    try:
        return jwt.decode(
                    jwt=token,
                    algorithms=[loginsettings.algorithm],
                    key=loginsettings.get_signature
                )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Expired Token"
        )
    
    except jwt.PyJWTError:
        return None