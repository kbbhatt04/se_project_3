
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
from fastapi import FastAPI
from pydantic import BaseModel, Field
from pymongo.mongo_client import MongoClient
from typing import Optional
from datetime import datetime
import requests
import time

# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

# try:
#     sender_email = "edumerge.noti@gmail.com"
#     receiver_email = "pathakutkarsh2615@gmail.com"
#     # password = "adminadmin123"

#     message = MIMEMultipart()
#     message['From'] = sender_email
#     message['To'] = receiver_email
#     message['Subject'] = 'Test mail'

#     body = 'This is a test email.'
#     message.attach(MIMEText(body, 'plain'))

#     mail_server = smtplib.SMTP('localhost')
#     # mail_server.login(sender_email, password)
#     mail_server.send_message(message)
#     mail_server.quit()

#     print("Successfully sent")

# except Exception as e:
#     print('Error:', e)

DATABASE_URL = "mongodb+srv://admin:UVdztRHHWkQC9atH@cluster0.v6xpxbx.mongodb.net/"
LOAD_BALANCER_URL = "http://localhost:4000"
SERVICE_REGISTRY_URL = "http://localhost:6000"

PING_THRESHOLD = 3
WAIT_TIME=10

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

def get_all_services():
    db = get_db()
    service_collection = db["service_registry"]
    services = service_collection.find()
    return list(services)
    
# health_check db
# { service_id,service_name, missed_ping_count, last_ping_time, status}

#monitor health of all services by sending a request to each service
def monitor_health():
    db=get_db()
    while True: 
        services = get_all_services()
        for service in services:
            service_url = service['service_url'] + "/health"
            response = requests.get(service_url)  #pinging
            if response.status_code != 200:
                health_check_collection = db["health_check"]
                instance_health_record = health_check_collection.find_one({"service_id": service['id']})
                if not instance_health_record:
                    instance_health_record = {
                        "service_id": service['id'],
                        "service_name": service['service_name'],
                        "missed_ping_count": 1,
                        "last_ping_time": datetime.now(),
                        "status": "DOWN"
                    }
                    health_check_collection.insert_one(instance_health_record)
                elif instance_health_record['missed_ping_count'] == PING_THRESHOLD:
                    #write an email to edumerge.noti@gmail.com
                    logger.log(message=f"Service: {service['service_name']}, ID: {instance_health_record['service_id']} is down!", level='error')
                    print(f"Service: {service['service_name']} is down!")

                    #notify service registry
                    response = requests.get(f"{SERVICE_REGISTRY_URL}/deregister_service/{service['id']}")
                    if response.status_code != 200:
                        logger.log(message=f"Failed to deregister at service registry | service: {service['service_name']}, id: {service['id']}", level='error')
                        print(f"Failed to deregister at service registry | service: {service['service_name']}, id: {service['id']}")

                    #notify load balancer
                    response = requests.get(f"{LOAD_BALANCER_URL}/deregister_service/{service['id']}")
                    if response.status_code != 200:
                        logger.log(message=f"Failed to deregister at load balancer | service: {service['service_name']}, id: {service['id']}", level='error')
                        print(f"Failed to deregister at load balancer | service: {service['service_name']}, id: {service['id']}")
                    

                else:
                    instance_health_record['missed_ping_count'] += 1
                    instance_health_record['last_ping_time'] = datetime.now()
                    instance_health_record['status'] = "DOWN"
                    health_check_collection.update_one({"service_id": service['id']}, {"$set": instance_health_record})
                
                    logger.log(message=f"Failed to connect to service: {service['service_name']}, id: {service['id']}", level='error')
                    print(f"Failed to connect to service: {service['service_name']}, id: {service['id']}")

            else:
                logger.log(message=f"Service: {service['service_name']}, id: {service['id']} is healthy", level='info')
                print(f"Service: {service['service_name']} is healthy")
        
        threading.Timer(WAIT_TIME, monitor_health).start()

if __name__ == "__main__":
    import uvicorn
    import threading
    threading.Thread(target=monitor_health).start()
    print("Starting health monitor subsystem...")
    # monitor_health()
    uvicorn.run("health_monitor_subsystem:app", host="0.0.0.0", port=7000)