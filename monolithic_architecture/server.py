from bson import ObjectId
from fastapi import FastAPI
from pydantic import BaseModel, Field
from pymongo.mongo_client import MongoClient
from typing import Optional

DATABASE_URL = "mongodb+srv://admin:admin@courses.2nficpj.mongodb.net/?retryWrites=true&w=majority"

def get_db(db_name):
    try:
        client = MongoClient(DATABASE_URL)
        db = client[db_name]
        return db
    except Exception as e:
        print(e)


app = FastAPI()

class Course(BaseModel):
    _id: str
    id: str
    title: str
    description: str
    instructor: str
    platform: str
    level: str
    url: str
    num_enrolled_students: int
    num_chapters: int
    is_paid: bool
    price: float

class Review(BaseModel):
    user_id: str
    course_id: str
    rating: int
    review: str


@app.get("/courses", response_model=list[Course])
async def get_courses(search: str = None, platform: str = None):
    db = get_db("courses_db")
    courses_collection = db["courses"]
    courses = list(courses_collection.find())

    print(search)
    if search:
        courses = [c for c in courses if search.strip().lower() in c["title"].lower() or search in c["description"].lower()]
    print(platform)
    if platform:
        courses = [c for c in courses if platform.strip().lower() == c["platform"].lower()]

    print(courses)

    for c in courses:
        c["_id"] = str(c["_id"])
        c["id"] = str(c["_id"])

    print(courses)

    return courses

@app.post("/enrollments/{course_id}")
def enroll_student(course_id: str, user_id: str):
    db = get_db("learning_db")
    enrollments_collection = db["enrollment"]
    enrollment_data = {"user_id": user_id, "course_id": course_id}
    # Check if user is already enrolled
    existing_enrollment = enrollments_collection.find_one(
        {"user_id": user_id, "course_id": course_id}
    )
    if existing_enrollment:
        raise HTTPException(status_code=400, detail="User already enrolled in this course")

    # Enroll student (if validations pass)
    enrollment_data = {"user_id": user_id, "course_id": course_id}
    enrollments_collection.insert_one(enrollment_data)

    return {"message": "Enrolled successfully"}



@app.post("/add_review")
async def add_review(review: Review):
    db = get_db("reviews_db")
    reviews_collection = db["reviews"]

    # Insert the review data
    reviews_collection.insert_one(review.dict())

    return {"message": "Review added successfully"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server:app", host="0.0.0.0", port=8000)