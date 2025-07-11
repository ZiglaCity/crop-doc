from jose import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
import os

load_dotenv()

security = HTTPBearer()
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        scheme = credentials.scheme

        # scheme, token = authorization.split()
        print(scheme, token)
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=403, detail="Invalid auth scheme")

        payload = jwt.decode(
            token,
            SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            options={"verify_aud": False},
            # audience = "authenticated" l#in prod, interchange this with the options
        )        
        # just for development purpose, return a valid user id, which is my id i created
        return "f6bc3aa5-2275-437f-95fd-dc321bde2b34"
        return payload["sub"] 

    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized")
