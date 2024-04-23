
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
from fastapi import FastAPI
from pydantic import BaseModel, Field
from pymongo.mongo_client import MongoClient
from typing import Optional
from datetime import datetime


# DATABASE_URL = "mongodb+srv://admin:UVdztRHHWkQC9atH@cluster0.v6xpxbx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# DATABASE_URL = "mongodb+srv://admin:veYwlbMIDu8cZ4ds@cluster0.axfu4kj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DATABASE_URL = "mongodb+srv://admin:veYwlbMIDu8cZ4ds@cluster0.axfu4kj.mongodb.net/"

class Logger:
    def __init__(self, db_name='logs_db', collection_name='logs', host='localhost'):
        self.client = MongoClient(DATABASE_URL)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def log(self, service_name, message, level='info'):
        timestamp = datetime.now()
        log_entry = {'timestamp': timestamp, 'message': message, 'service_name': service_name, 'level': level}
        self.collection.insert_one(log_entry)

    def close(self):
        self.client.close()

def get_db():
    try:
        client = MongoClient(DATABASE_URL)
        db = client["new"]
        print("Connected to MongoDB!")
        return db
    except Exception as e:
        print(e)
        print("Failed to connect to MongoDB!")

app = FastAPI()
logger=Logger()

class Service(BaseModel):
    service_name: str
    service_url: str

@app.post("/register_service")
async def register_service(service: Service):
    db = get_db()
    service_collection = db["service_registry"]
    service = service.model_dump()
    service_id = service_collection.insert_one(service).inserted_id
    print(f"Service registered successfully with ID: {service_id}")
    logger.log(service_name=service["service_name"], message=f"Service registered successfully with ID: {service_id}", level='info')
    return {"message": "Service registered successfully!"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("service_registry_subsystem:app", host="0.0.0.0", port=8000)