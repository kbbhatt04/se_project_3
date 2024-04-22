from pymongo import MongoClient

uri = "mongodb+srv://user:user@se-p3.ti1zbcm.mongodb.net/?retryWrites=true&w=majority&appName=SE-P3"

client = MongoClient(uri)
db = client.users_db

collection_name = db["users_db"]
