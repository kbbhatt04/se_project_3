from bson import ObjectId
from fastapi import FastAPI
from pydantic import BaseModel
from pymongo.mongo_client import MongoClient

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
    title: str
    description: str
    instructor: str
    platform: str
    level: str
    url: str


@app.post("/add_course", response_model=Course)
def add_course(course: Course):
    db = get_db()
    courses_collection = db["courses"]

    course = course.dict()
    course_id = courses_collection.insert_one(course).inserted_id

    return courses_collection.find_one({"_id": course_id})


@app.delete("/delete_course/{course_id}")  # Use 204 No Content for deletions
def delete_course(course_id: str):
    db = get_db()
    courses_collection = db["courses"]

    print(ObjectId(course_id), type(ObjectId(course_id)))
    delete_result = courses_collection.delete_one({"_id": ObjectId(course_id)})

    if delete_result.deleted_count == 1:
        return {"message": f"Course with ID {course_id} deleted successfully"}
    else:
        return {"message": f"Course with ID {course_id} not found"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("course_management_subsystem:app", host="0.0.0.0", port=8000)
