import re
import jwt
from datetime import datetime, timedelta
import os
from fastapi import FastAPI, Body, HTTPException, Depends, Header
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel,EmailStr, ValidationError
from pymongo import MongoClient

from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError

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

def create_jwt(payload,secret_key):
    algorithm = 'HS256'
    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token

@app.get("/protected")
async def protected_route(credentials: HTTPAuthorizationCredentials = Depends(security)):
    print(credentials)
    decoded_token = await validate(credentials)
    email = decoded_token.get("email")
    role = decoded_token.get("role")
    return {"message": "This is a protected route", "email": email, "role": role}

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
        return {"token": jwt_token}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    

# @app.post("/validate")
# async def validate(authorization: str = Header(...)):
#     if not authorization: 
#         raise HTTPException(status_code=401, detail="Missing credentials")
#     print("\n" + "="*20 + " " + "="*20 + "\n")
#     print(authorization)
#     print("\n" + "="*40 + "\n")
#     if len(authorization.split(" ")) != 2 or authorization.split(" ")[0].lower() != "bearer":
#         raise HTTPException(status_code=401, detail="Invalid Authorization header")
#     encoded_jwt=authorization.split(" ")[1]
#     if not encoded_jwt: 
#         raise HTTPException(status_code=401, detail="Missing credentials")
    
#     try:
#         decoded = jwt.decode(
#             encoded_jwt, JWT_SECRET, algorithms=["HS256"]
#         )
#     except:
#         raise HTTPException(status_code=403, detail="Invalid token")
#     return decoded

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


if client is not None:
    print("Successfully connected to MongoDB")
else:
    print("fuck")
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
