import requests
from fastapi import FastAPI, HTTPException
from pymongo.mongo_client import MongoClient

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
        learningmanagement = LearningManagement()
        enrollments_collection = LearningManagement._db["enrollment"]
        enrollment_data = {"user_id": user_id, "course_id": course_id}

        existing_enrollment = enrollments_collection.find_one(
            {"user_id": user_id, "course_id": course_id}
        )
        if existing_enrollment:
            raise HTTPException(status_code=400, detail="User already enrolled in this course")

        url = f"http://localhost:8004/payment"
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
        learningmanagement = LearningManagement()
        progress_collection = LearningManagement._db["progress"]

        url = f"http://localhost:8000/courses/{course_id}"

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


@app.post("/enrollments")
def enroll_student(course_id: str, user_id: str, payment_method: str):
    return LearningManagement.enroll_student(course_id, user_id, payment_method)


@app.post("/progress")
def track_progress(course_id: str, user_id: str):
    return LearningManagement.track_progress(course_id, user_id)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("learning_management_subsystem:app", host="0.0.0.0", port=8003)
