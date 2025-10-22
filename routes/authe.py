from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
 
 from app.server.jwt_handler import create_access_token
 
 router = APIRouter()
 
 class LoginRequest(BaseModel):
        username: str
        password: str
        
@router.post("/login")
async def login(data: LoginRequest):
    if data.username == "admin" and data.password == "123":
        token = create_access_token({"sub": data.username})
        return {"access_token": token}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")