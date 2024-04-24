
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


class Logger:
    def __init__(self, db_name='logs_db', collection_name='logs', host='localhost'):
        self.client = MongoClient(DATABASE_URL)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def log(self, message, level='info', service_name = "LOAD BALANCER"):
        timestamp = datetime.now()
        log_entry = {'timestamp': timestamp, 'message': message, 'service_name': service_name, 'level': level}
        self.collection.insert_one(log_entry)

    def close(self):
        self.client.close()

def get_db():
    try:
        client = MongoClient(DATABASE_URL)
        db = client["load_balancer_db"]
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
    service['deleted'] = False
    service_id = service_collection.insert_one(service).inserted_id
    print(f"{service.service_name} instance registered successfully with ID: {service_id}")
    logger.log(service_name="LOAD BALANCER", message=f"{service.service_name} instance registered successfully with ID: {service_id}", level='info')
    return {"message": "Service instance registered successfully!"}


async  def route_request(service_type, instance, body, path):
    service_url = instance['service_url'] + "/" + path
    if service_type == "GET":
        response = requests.get(service_url)
    elif service_type == "POST":
        response = requests.post(service_url, json=body)
    return response.json()

class Request(BaseModel):
    service_type: str #GET, POST
    service_name: str #service name
    body: Optional[dict] = None
    path: str

@app.post("/balance_load")
async def balance_load(request: Request):
    service_name = request.service_name
    service_type = request.service_type
    body = request.body
    path = request.path

    #getting available instances
    db = get_db()
    service_collection = db["service_registry"]
    instances = service_collection.find({"service_name": service_name}, {"deleted": False})
    instances = list(instances)
    instances_count = len(instances)

    if instances_count == 0:
        logger.log(message=f"No instances found for {service_name} service!", level='error')
        return {"message": "No instances found for the service!"}
    else:
        logger.log(message=f"Total instances found for {service_name} service: {instances_count}", level='info')
        
        load_balancing_collection = db["load_balancing"]
        load_balancing = load_balancing_collection.find_one({"service_name": service_name})
        instances_index = 0
        if load_balancing:
            instances_index = load_balancing['last_instance_index']
            instances_index = (instances_index + 1) % instances_count #simple round robin
            load_balancing_collection.update_one({"service_name": service_name}, {"$set": {"last_instance_index": instances_index}})
        else:
            load_balancing_collection.insert_one({"service_name": service_name, "last_instance_index": instances_index})

        instance = instances[instances_index]
        
        logger.log(message=f"Load balanced to {service_name} instance with ID: {instance['id']}", level='info')

        return route_request(service_type, instance, body, path)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("service_registry_subsystem:app", host="0.0.0.0", port=8000)