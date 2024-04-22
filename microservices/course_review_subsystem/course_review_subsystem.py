from fastapi import FastAPI
from pydantic import BaseModel, Field
from pymongo.mongo_client import MongoClient
from typing import Optional

DATABASE_URL = "mongodb+srv://admin:admin@courses.2nficpj.mongodb.net/?retryWrites=true&w=majority"


def get_db():
    try:
        client = MongoClient(DATABASE_URL)
        db = client["reviews_db"]
        return db
    except Exception as e:
        print(e)


app = FastAPI()


class Review(BaseModel):
    learner_id: str
    course_id: str
    rating: int
    review: str


@app.post("/add_review")
async def add_review(review: Review):
    db = get_db()
    reviews_collection = db["reviews"]

    # Insert the review data
    reviews_collection.insert_one(review.dict())

    return {"message": "Review added successfully"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("course_exploration_subsystem:app", host="0.0.0.0", port=8000)