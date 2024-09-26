from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from supabase import create_client, Client
import os

router = APIRouter()

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

class UserRegistration(BaseModel):
    username: str
    password: str
    email: str

class UserLogin(BaseModel):
    email: str
    password: str

@router.get("/test/")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

@router.post("/register/")
async def register_user(user: UserRegistration):
    response = supabase.auth.sign_up(email=user.email, password=user.password)
    if response['error']:
        raise HTTPException(status_code=400, detail=response['error']['message'])
    
    user_id = response['data']['id']
    user_info = {
        "user_uid": user_id,
        "username": user.username,
        "email": user.email
    }
    supabase.table('Users').upsert(user_info).execute()
    return {"message": "User registered successfully", "user_id": user_id}

@router.get("/login/")
async def login_user(user: UserLogin):
    response = supabase.auth.sign_in(email=user.email, password=user.password)
    if response['error']:
        raise HTTPException(status_code=400, detail=response['error']['message'])
    return {"message": "User logged in successfully", "access_token": response['data']['access_token']}