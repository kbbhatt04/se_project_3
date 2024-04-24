import sys

sys.path.append("../microservices")
from fastapi import FastAPI
from pymongo.mongo_client import MongoClient
from microservices.models import Review

DATABASE_URL = "mongodb+srv://admin:admin@courses.2nficpj.mongodb.net/?retryWrites=true&w=majority"


def get_db():
    try:
        client = MongoClient(DATABASE_URL)
        db = client["reviews_db"]
        return db
    except Exception as e:
        print(e)


app = FastAPI()


class CourseReview:
    _db = None

    def __init__(self):
        try:
            DATABASE_URL = "mongodb+srv://admin:admin@courses.2nficpj.mongodb.net/?retryWrites=true&w=majority"
            client = MongoClient(DATABASE_URL)
            CourseReview._db = client["reviews_db"]
        except Exception as e:
            print(e)

    @staticmethod
    def add_review(review: Review):
        course_review = CourseReview()
        reviews_collection = CourseReview._db["reviews"]

        reviews_collection.insert_one(review.dict())

        return {"message": "Review added successfully"}

    @staticmethod
    def get_course_reviews(course_id: str):
        course_review = CourseReview()
        reviews_collection = CourseReview._db["reviews"]

        course_reviews = reviews_collection.find({"course_id": course_id})

        avg_rating = 0
        reviews_list = []
        for i in course_reviews:
            i["_id"] = str(i["_id"])
            reviews_list += i,
            avg_rating += int(i["rating"])

        avg_rating /= len(reviews_list)

        return reviews_list, avg_rating, len(reviews_list)

    @staticmethod
    def get_average_ratings():
        course_review = CourseReview()
        reviews_collection = CourseReview._db["reviews"]

        pipeline = [
            {"$group": {"_id": "$course_id", "average_rating": {"$avg": "$rating"}}}
        ]
        average_ratings = list(reviews_collection.aggregate(pipeline))

        for rating in average_ratings:
            rating["_id"] = str(rating["_id"])

        return average_ratings


@app.post("/add_review")
def add_review(review: Review):
    return CourseReview.add_review(review)


@app.get("/get_reviews/{course_id}")
def get_course_reviews(course_id: str):
    return CourseReview.get_course_reviews(course_id)


@app.get("/reviews/average_ratings")
def get_average_ratings():
    return CourseReview.get_average_ratings()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("course_review_subsystem:app", host="0.0.0.0", port=8002)
