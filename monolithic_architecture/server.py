from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo.mongo_client import MongoClient

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
    url: list
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
def get_courses():
    db = get_db("courses_db")
    courses_collection = db["courses"]
    courses = list(courses_collection.find())

    for c in courses:
        c["_id"] = str(c["_id"])
        c["id"] = str(c["_id"])

    print(courses)

    return courses


@app.post("/enroll")
def enroll(course_id: str, user_id: str):
    db = get_db("learning_db")
    enrollments_collection = db["enrollment"]
    enrollment_data = {"user_id": user_id, "course_id": course_id}

    existing_enrollment = enrollments_collection.find_one(enrollment_data)
    if existing_enrollment:
        raise HTTPException(status_code=400, detail="User already enrolled in this course")

    enrollments_collection.insert_one(enrollment_data)

    return {"message": "Enrolled successfully"}


@app.post("/add_review")
def add_review(review: Review):
    db = get_db("reviews_db")
    reviews_collection = db["reviews"]

    reviews_collection.insert_one(review.dict())

    return {"message": "Review added successfully"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server:app", host="0.0.0.0", port=8000)
