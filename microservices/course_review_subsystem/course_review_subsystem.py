from bson import ObjectId
from fastapi import FastAPI
from pydantic import BaseModel
from pymongo.mongo_client import MongoClient

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
    user_id: str
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


@app.get("/get_reviews/{course_id}")
def get_course_reviews(course_id: str):
    db = get_db()
    reviews_collection = db["reviews"]

    course_reviews = reviews_collection.find({"course_id": course_id})

    avg_rating = 0
    reviews_list = []
    for i in course_reviews:
        i["_id"] = str(i["_id"])
        reviews_list += i,
        avg_rating += int(i["rating"])

    avg_rating /= len(reviews_list)

    return reviews_list, avg_rating, len(reviews_list)


@app.get("/reviews/average_ratings")
def get_average_ratings():
    db = get_db()
    reviews_collection = db["reviews"]

    # Use aggregation pipeline to group by course_id, calculate average rating
    pipeline = [
        {"$group": {"_id": "$course_id", "average_rating": {"$avg": "$rating"}}}
    ]
    average_ratings = list(reviews_collection.aggregate(pipeline))

    # Convert ObjectId to string (if needed for frontend)
    for rating in average_ratings:
        rating["_id"] = str(rating["_id"])

    return average_ratings


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("course_review_subsystem:app", host="0.0.0.0", port=8000)
