import re
import jwt
from datetime import datetime, timedelta
import os
from fastapi import FastAPI, Body, HTTPException, Depends, Header
# from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel,EmailStr, ValidationError
from pymongo import MongoClient
from fastapi.responses import JSONResponse, Response
from fastapi.responses import JSONResponse
from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import random
import uuid



# from jose import JWTError

# put variables into env include jwt secret

MONGO_URI = "mongodb://localhost:27017"
client = MongoClient(MONGO_URI)
db = client["project3"]
users_collection = db["auths"]
app = FastAPI()

security = HTTPBearer()
JWT_SECRET ="asdasdasd"

class User(BaseModel):
    email: EmailStr
    role: str
    password: str

class Credential(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    token: str

def create_jwt(payload,secret_key,expires_in_minutes=10):
    algorithm = 'HS256'
    expiration = datetime.utcnow() + timedelta(minutes=expires_in_minutes)
    payload.update({"exp": expiration})
    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token


@app.get("/protected")
async def protected_route(credentials: HTTPAuthorizationCredentials = Depends(security)):
    print(credentials)
    decoded_token = await validate(credentials)
    email = decoded_token.get("email")
    role = decoded_token.get("role")
    return {"message": "This is a protected route", "email": email, "role": role}

sessions={}
def create_session(user_email:str):
    session_id = str(len(sessions) + random.randint(0, 1000000))
    while session_id in sessions:
        session_id = len(sessions) + random.randint(0, 1000000)
    sessions[session_id] = {"email": user_email}
    return session_id
def get_user_from_session_id(session_id_b: str):
    if session_id_b in sessions:
        return session_id_b
    else:
        raise HTTPException(status_code=401, detail="Invalid session ID")

@app.get("/me")
def read_current_user(session_id: str = Depends(get_user_from_session_id)):
    return {"session_id": session_id}

@app.post("/login")
async def login(credentials:Credential):
    print(credentials)
    user = users_collection.find_one({"email": credentials.email})
    if user and user["password"] == credentials.password:
        print("\n" + "="*20 + " " + "="*20 + "\n")
        print(user)
        print("\n" + "="*40 + "\n")
        payload = {"email": credentials.email,"role":user["role"]}
        jwt_token = create_jwt(payload, JWT_SECRET)
        response = JSONResponse({"token": jwt_token})
        session_id = create_session(credentials.email)
        print("\n" + "="*20 + " " + "="*20 + "\n")
        print("session id",session_id)
        print("\n" + "="*40 + "\n")
        response.set_cookie(key="session_id", value=session_id)
        response.set_cookie(key="jwt_token", value=jwt_token, httponly=True)
        return response
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/validate")
async def validate(credentials: HTTPAuthorizationCredentials= Depends(security)):
    if not credentials: 
        raise HTTPException(status_code=401, detail="Missing credentials")
    
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid Authorization scheme")

    encoded_jwt = credentials.credentials
    
    if not encoded_jwt: 
        raise HTTPException(status_code=401, detail="Missing credentials")
    try:
        decoded = jwt.decode(
            encoded_jwt, JWT_SECRET, algorithms=["HS256"]
        )
    except:
        raise HTTPException(status_code=403, detail="Invalid token")
    return decoded

@app.post("/signup")
async def signup(user: User):
    print("\n", user)
    existing_user = users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    try:
        user_data = user.dict()
        print(user_data)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # if len(user_data['password']) < 8:
    #     raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")

    # # Check password strength
    # if len(user_data['password']) < 8 or not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$', user_data['password']):
    #     raise HTTPException(status_code=400, detail="Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character")

    users_collection.insert_one(user_data)

    return {"message": "User signed up successfully"}


@app.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="session_id")
    response.delete_cookie(key="jwt_token")
    return {"message": "Logout successful"}

if client is not None:
    print("Successfully connected to MongoDB")
else:
    print("errro")
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)