
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
from fastapi import FastAPI
from pydantic import BaseModel, Field
from pymongo.mongo_client import MongoClient
from typing import Optional

DATABASE_URL = "mongodb+srv://admin:UVdztRHHWkQC9atH@cluster0.v6xpxbx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
def get_db():
    try:
        client = MongoClient(DATABASE_URL)
        db = client["service_registry_db"]
        print("Connected to MongoDB!")
        return db
    except Exception as e:
        print(e)
        print("Failed to connect to MongoDB!")

def send_log(log: str):
    db = get_db()
    log_collection = db["log"]
    log_id = log_collection.log.insert_one(log).inserted_id
    print(f"Log sent successfully with ID: {log_id}")
    return {"message": "Log sent successfully!"}

app = FastAPI()

class Service(BaseModel):
    service_name: str
    service_url: str

@app.post("/register_service")
async def register_service(service: Service):
    db = get_db()
    service_collection = db["service_registry"]
    service = service.dict()
    service_id = db.service_registry.insert_one(service).inserted_id
    print(f"Service registered successfully with ID: {service_id}")
    send_log(f"Service registered successfully with ID: {service_id}")
    return {"message": "Service registered successfully!"}

# Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)


# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run("course_exploration_subsystem:app", host="0.0.0.0", port=8000)

db=get_db()