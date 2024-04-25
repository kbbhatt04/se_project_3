
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
SERVICE_REGISTRY_URL = "http://localhost:8000"

class Logger:
    def __init__(self, db_name='logs_db', collection_name='logs', host='localhost'):
        self.client = MongoClient(DATABASE_URL)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def log(self,  message, level='info', service_name = "HEALTH MONITOR"):
        timestamp = datetime.now()
        log_entry = {'timestamp': timestamp, 'message': message, 'service_name': service_name, 'level': level}
        self.collection.insert_one(log_entry)

    def close(self):
        self.client.close()


def get_db():
    try:
        client = MongoClient(DATABASE_URL)
        db = client["health_monitor_db"]
        print("Connected to MongoDB!")
        return db
    except Exception as e:
        print(e)
        print("Failed to connect to MongoDB!")

app = FastAPI()
logger=Logger()

class Service(BaseModel):
    id: str
    service_name: str
    service_url: str

# this will be called by service registry subsystem to register a service
@app.post("/register_service")
async def register_service(service: Service):
    db = get_db()
    service_collection = db["service_registry"]
    service = service.model_dump()

    print(service)
    service['deleted'] = False
    service_id = service_collection.insert_one(service).inserted_id
    print(f"{service['service_name']} instance registered successfully with ID: {service_id}")
    logger.log( message=f"{service['service_name']} instance registered successfully with ID: {service_id}", level='info')
    return {"message": "Service instance registered successfully!", "id": str(service_id)}

async def get_all_services():
    db = get_db()
    service_collection = db["service_registry"]
    services = service_collection.find()
    return services

