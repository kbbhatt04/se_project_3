# from fastapi import Depends, FastAPI, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from jose import JWTError, jwt
# from typing import Optional
# from pymongo.mongo_client import MongoClient
# from passlib.context import CryptContext
# from datetime import datetime, timedelta
# from pydantic import BaseModel
# import uvicorn

# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
# SECRET_KEY = "2a6a537d33a78f8911daf8532a7ed6f95619bb07bb04aa3111d5dd773cebbeb9"
# MONGO_URI = "mongodb+srv://user:user@se-p3.ti1zbcm.mongodb.net/?retryWrites=true&w=majority&appName=SE-P3"

# class User(BaseModel):
#     username: str
#     hashed_password: str
#     email: str


# app = FastAPI()

# users_db = {
#     "user1": {
#         "username": "user1",
#         "hashed_password": "user1",
#         "email": "user1@gmail.com"
#     }
# }


# def get_db():
#     try:
#         client = MongoClient(MONGO_URI)
#         db = client["user_db"]
#         return db
#     except Exception as e:
#         print(e)


# # Function to create JWT token
# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


# # Password hashing
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # Function to verify password
# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# def get_user(username: str):
#     for user in users_db:
#         if user.username == username:
#             return user


# # Function to authenticate user
# def authenticate_user(username: str, password: str):
#     user = get_user(username)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user

# # OAuth2 password flow
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# # Endpoint to generate JWT token
# @app.post("/token")
# async def login_for_access_token(username: str, password: str):
#     user = authenticate_user(username, password)
#     if not user:
#         raise HTTPException(status_code=401, detail="Invalid username or password")
#     access_token = create_access_token(data={"sub": user.username})
#     return {"access_token": access_token, "token_type": "bearer"}

# @app.post("/users/")
# async def create_user(user: User):
#     hashed_password = pwd_context.hash(user.password)
#     users_db.append(User(username=user.username, email=user.email, hashed_password=hashed_password))
#     return user

# @app.get("/")
# async def read_root():
#     return {"message": "Welcome to the authentication API"}

# if __name__ == "__main__":
#     uvicorn.run("auth:app", host="localhost", port=8000)

