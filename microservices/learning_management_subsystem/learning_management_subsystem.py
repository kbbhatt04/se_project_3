import os

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo.mongo_client import MongoClient

load_dotenv()

app = FastAPI()


class LearningManagement:
    _db = None

    def __init__(self):
        try:
            DATABASE_URL = "mongodb+srv://admin:admin@courses.2nficpj.mongodb.net/?retryWrites=true&w=majority"
            client = MongoClient(DATABASE_URL)
            LearningManagement._db = client["learning_db"]
        except Exception as e:
            print(e)

    @staticmethod
    def enroll_student(course_id: str, user_id: str, payment_method: str):
        learning_management = LearningManagement()
        enrollments_collection = LearningManagement._db["enrollment"]
        enrollment_data = {"user_id": user_id, "course_id": course_id}

        existing_enrollment = enrollments_collection.find_one(
            {"user_id": user_id, "course_id": course_id}
        )
        if existing_enrollment:
            raise HTTPException(status_code=400, detail="User already enrolled in this course")

        url = f"http://localhost:{os.getenv('payments_subsystem')}/payment"
        data = {"course_id": course_id, "user_id": user_id, "payment_method": payment_method}
        response = requests.post(url, json=data)
        print(response, response.text)
        if response.status_code == 200:
            message = response.json()["message"]
            print(message)

        enrollment_data = {"user_id": user_id, "course_id": course_id}
        enrollments_collection.insert_one(enrollment_data)

        return {"message": "Enrolled successfully"}

    @staticmethod
    def track_progress(course_id: str, user_id: str):
        learning_management = LearningManagement()
        progress_collection = LearningManagement._db["progress"]

        url = f"http://localhost:{os.getenv('course_exploration_subsystem')}/courses/{course_id}"

        response = requests.get(url)
        if response.status_code == 200:
            course = response.json()
            course_num_units = course["num_chapters"]
            completed_units = progress_collection.find_one({"user_id": user_id, "course_id": course_id})
            return {
                "completion_percentage": len(list(completed_units["progress_details"].keys())) * 100 / course_num_units}
        else:
            print(f"Error: {response.status_code}")
            return {"error": response.status_code}

    @staticmethod
    def add_to_progress(course_id: str, user_id: str, chapter: int):
        learning_management = LearningManagement()
        progress_collection = LearningManagement._db["progress"]
        progress_data = {"user_id": user_id, "course_id": course_id}
        res = progress_collection.find_one(progress_data)
        res["progress_details"][str(chapter)] = True

        newvalues = {"$set": {"progress_details": res["progress_details"]}}

        progress_collection.update_one(progress_data, newvalues)

        return {"message": "Progress updated"}

    @staticmethod
    def remove_from_progress(course_id: str, user_id: str, chapter: int):
        learning_management = LearningManagement()
        progress_collection = LearningManagement._db["progress"]
        progress_data = {"user_id": user_id, "course_id": course_id}
        res = progress_collection.find_one(progress_data)
        del (res["progress_details"][str(chapter)])

        newvalues = {"$set": {"progress_details": res["progress_details"]}}

        progress_collection.update_one(progress_data, newvalues)

        return {"message": "Progress updated"}


@app.post("/enroll_student")
def enroll_student(course_id: str, user_id: str, payment_method: str):
    return LearningManagement.enroll_student(course_id, user_id, payment_method)


@app.post("/track_progress")
def track_progress(course_id: str, user_id: str):
    return LearningManagement.track_progress(course_id, user_id)


@app.post("/add_to_progress")
def add_to_progress(course_id: str, user_id: str, chapter: int):
    return LearningManagement.add_to_progress(course_id, user_id, chapter)


@app.post("/remove_from_progress")
def remove_from_progress(course_id: str, user_id: str, chapter: int):
    return LearningManagement.remove_from_progress(course_id, user_id, chapter)


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

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("learning_management_subsystem:app", host="0.0.0.0",
                port=int(os.getenv("learning_management_subsystem")))
