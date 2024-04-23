from bson import ObjectId
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo.mongo_client import MongoClient

DATABASE_URL = "mongodb+srv://admin:admin@courses.2nficpj.mongodb.net/?retryWrites=true&w=majority"


def get_db():
    try:
        client = MongoClient(DATABASE_URL)
        db = client["learning_db"]
        return db
    except Exception as e:
        print(e)


app = FastAPI()


class Progress(BaseModel):
    student_id: str
    course_id: str
    completion_status: str  # "completed" or "in progress"
    progress_details: dict  # Stores completed modules, quiz scores, etc.


@app.post("/enrollments/{course_id}")
def enroll_student(course_id: str, user_id: str):
    # Check if user is already enrolled or course is open
    # ... (logic for enrollment validation)
    db = get_db()
    enrollments_collection = db["enrollment"]
    enrollment_data = {"student_id": user_id, "course_id": course_id}
    # Check if user is already enrolled
    existing_enrollment = enrollments_collection.find_one(
        {"student_id": user_id, "course_id": course_id}
    )
    if existing_enrollment:
        raise HTTPException(status_code=400, detail="User already enrolled in this course")

    # Enroll student (if validations pass)
    enrollment_data = {"student_id": user_id, "course_id": course_id}
    enrollments_collection.insert_one(enrollment_data)

    return {"message": "Enrolled successfully"}


@app.post("/progress")
def track_progress(progress: Progress):
    # Update progress document for the student and course
    # ... (logic to update progress_details based on user actions)
    return {"message": "Progress updated"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("learning_management_subsystem:app", host="0.0.0.0", port=8000)