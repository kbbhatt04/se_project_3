from fastapi import FastAPI
from pydantic import BaseModel, Field
from pymongo.mongo_client import MongoClient
from typing import Optional

DATABASE_URL = "mongodb+srv://admin:admin@courses.2nficpj.mongodb.net/?retryWrites=true&w=majority"


def get_db():
    try:
        client = MongoClient(DATABASE_URL)
        db = client["courses_db"]
        return db
    except Exception as e:
        print(e)


app = FastAPI()


class Course(BaseModel):
    id: Optional[str] = None
    title: str
    description: str
    instructor: str
    platform: str
    level: str
    url: str
    num_enrolled_students: int
    price: float


@app.get("/courses", response_model=list[Course])
async def get_courses(search: str = None, platform: str = None):
    db = get_db()
    courses_collection = db["courses"]
    courses = list(courses_collection.find())

    print(search)
    if search:
        courses = [c for c in courses if search.strip().lower() in c["title"].lower() or search in c["description"].lower()]
    print(platform)
    if platform:
        courses = [c for c in courses if platform.strip().lower() == c["platform"].lower()]

    return courses

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("course_exploration_subsystem:app", host="0.0.0.0", port=8000)
