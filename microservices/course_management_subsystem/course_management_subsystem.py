import sys

sys.path.append("../../microservices")

from bson import ObjectId
from fastapi import FastAPI
from pymongo.mongo_client import MongoClient
from fastapi.middleware.cors import CORSMiddleware
from models import Course
import requests

import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = "mongodb+srv://admin:admin@courses.2nficpj.mongodb.net/?retryWrites=true&w=majority"
SERVICE_REGISTRY_URL = f"http://localhost:{os.getenv('service_registry_subsystem')}"

app = FastAPI()


class CourseManagement:
    _db = None

    def __init__(self):
        try:
            DATABASE_URL = "mongodb+srv://admin:admin@courses.2nficpj.mongodb.net/?retryWrites=true&w=majority"
            client = MongoClient(DATABASE_URL)
            CourseManagement._db = client["courses_db"]
        except Exception as e:
            print(e)

    @staticmethod
    def add_course(course):
        course_management = CourseManagement()
        courses_collection = CourseManagement._db["courses"]

        course = course.dict()
        course_id = courses_collection.insert_one(course).inserted_id

        return courses_collection.find_one({"_id": course_id})

    @staticmethod
    def delete_course(course_id: str):
        course_management = CourseManagement()
        courses_collection = CourseManagement._db["courses"]

        print(ObjectId(course_id), type(ObjectId(course_id)))
        delete_result = courses_collection.delete_one({"_id": ObjectId(course_id)})

        if delete_result.deleted_count == 1:
            return {"message": f"Course with ID {course_id} deleted successfully"}
        else:
            return {"message": f"Course with ID {course_id} not found"}


@app.post("/add_course", response_model=Course)
def add_course(course: Course):
    return CourseManagement.add_course(course)


@app.delete("/delete_course/{course_id}")
def delete_course(course_id: str):
    return CourseManagement.delete_course(course_id)
origins = [
    "http://localhost",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

#generate heartbeat
@app.get("/health")
async def health():
    return {"message": "Service is up and running!"}

if __name__ == "__main__":
    import uvicorn
    requests.post(f"{SERVICE_REGISTRY_URL}/register_service", json={"service_name": "course_management_subsystem", "service_url": f"http://localhost:{os.getenv('course_management_subsystem')}"})
    uvicorn.run("course_management_subsystem:app", host="0.0.0.0", port=int(os.getenv('course_management_subsystem')))
