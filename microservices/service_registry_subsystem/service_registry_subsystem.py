
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
from fastapi import FastAPI
from pydantic import BaseModel, Field
from pymongo.mongo_client import MongoClient
from typing import Optional
from datetime import datetime
import requests
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = "mongodb+srv://admin:UVdztRHHWkQC9atH@cluster0.v6xpxbx.mongodb.net/"
LOAD_BALANCER_URL = f"http://localhost:{os.getenv('load_balancer_subsystem')}"
HEALTH_MONITOR_URL = f"http://localhost:{os.getenv('health_monitor_subsystem')}"

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
    service["deleted"] = False
    service_id = service_collection.insert_one(service).inserted_id

    response = requests.post(f"{LOAD_BALANCER_URL}/register_service_load_balancer", json={"service_name": service["service_name"], "service_url": service["service_url"], "id": str(service_id)})
    if response.status_code != 200:
        logger.log(message=f"Failed to update instance to load balancer service with ID: {service_id}", level='error')
        return {"message": "Failed to register service to load balancer!"}
    
    response = requests.post(f"{HEALTH_MONITOR_URL}/register_service_health_monitor", json={"service_name": service["service_name"], "service_url": service["service_url"], "id": str(service_id)})
    if response.status_code != 200:
        logger.log(message=f"Failed to register instance to health monitor service with ID: {service_id}", level='error')
        return {"message": "Failed to register service to health monitor!"}
    
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

#health monitor will notify load balancer about the service status
@app.get("/deregister_service/{service_id}")
async def deregister_service(service_id: str):
    db = get_db()
    service_collection = db["service_registry"]
    service_collection.update_one({"_id": service_id}, {"$set": {"deleted": True}})
    logger.log(message=f"{service_id} deregistered successfully!", level='info')
    return {"message": "Service instance deregistered successfully!"}

if __name__ == "__main__":
    import uvicorn
    print("Starting service registry subsystem")
    requests.get(f"{HEALTH_MONITOR_URL}/start_health_monitor")
    uvicorn.run("service_registry_subsystem:app", host="0.0.0.0", port=int(os.getenv('service_registry_subsystem')))