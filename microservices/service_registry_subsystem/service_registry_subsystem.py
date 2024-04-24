
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
from fastapi import FastAPI
from pydantic import BaseModel, Field
from pymongo.mongo_client import MongoClient
from typing import Optional
from datetime import datetime
import requests


DATABASE_URL = "mongodb+srv://admin:UVdztRHHWkQC9atH@cluster0.v6xpxbx.mongodb.net/"
LOAD_BALANCER_URL = "http://localhost:4000"

class Logger:
    def __init__(self, db_name='logs_db', collection_name='logs', host='localhost'):
        self.client = MongoClient(DATABASE_URL)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def log(self,  message, level='info', service_name = "SERVICE REGISTRY"):
        timestamp = datetime.now()
        log_entry = {'timestamp': timestamp, 'message': message, 'service_name': service_name, 'level': level}
        self.collection.insert_one(log_entry)

    def close(self):
        self.client.close()

def get_db():
    try:
        client = MongoClient(DATABASE_URL)
        db = client["service_registry_db"]
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
    service["created_at"] = datetime.now()
    service_id = service_collection.insert_one(service).inserted_id

    response = requests.post(f"{LOAD_BALANCER_URL}/register_service", json={"service_name": service["service_name"], "service_url": service["service_url"], "id": service_id})
    if response.status_code != 200:
        logger.log(message=f"Failed to update instance to load balancer service with ID: {service_id}", level='error')
        return {"message": "Failed to register service to load balancer!"}
    
    print(f"Service registered successfully with ID: {service_id}")
    logger.log( message=f"Service registered successfully with ID: {service_id}", level='info')
    return {"message": "Service registered successfully!"}

class GetService(BaseModel):
    service_name: str

@app.post("/get_service")
async def get_service(serviceQuery: GetService):
    db = get_db()
    service_collection = db["service_registry"]
    service_name = serviceQuery.service_name
    service = service_collection.find_one({"service_name": service_name})
    service['id'] = str(service['_id'])
    del(service['_id'])

    if service:
        logger.log(message=f"{service_name} service found successfully!", level='info')
        return service
    else:
        logger.log(message=f"{service_name} service not found!", level='error')
        return {"message": "Service not found!"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("service_registry_subsystem:app", host="0.0.0.0", port=8000)