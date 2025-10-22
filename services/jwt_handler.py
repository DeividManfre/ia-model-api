import jwt, datetime
import fastapi import Depends, HTTPException, Header

SCRET_KEY = "TEMPORARIO_KEY"

class JWTHandler:
    def __init__(self, secret_key: str = SECRET_KEY):
        self.secret_key = secret_key
        
    def create_access_token(self, data: dict, expires_delta: int = 30) -> str:
        to_encode = data.copy()
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_delta)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm="HS256")
        return encoded_jwt
    
    def verify_access_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")