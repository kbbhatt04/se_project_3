from fastapi import APIRouter
from models.users import User
from config.database import collection_name
from schema.user_schema import list_users
from bson import ObjectId

router = APIRouter()

# Get request
@router.get("/")
async def get_users():
    users = list_users(collection_name.find())
    return users


# Post request
@router.post("/")
async def post_user(user: User):
    collection_name.insert_one(dict(user))


# Put request
@router.post("/{id}")
async def update_user(id: str, user: User):
    collection_name.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(user)})

# Delete request
@router.delete("/{id}")
async def delete_user(id: str):
    collection_name.find_one_and_delete({"_id": ObjectId(id)})
