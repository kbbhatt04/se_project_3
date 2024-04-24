import sys

import requests

sys.path.append("../microservices")
from bson import ObjectId
from fastapi import FastAPI
from pymongo.mongo_client import MongoClient
from microservices.models import Course
from PlatformCriteria import PlatformCriteria
from LevelCriteria import LevelCriteria
from PriceCriteria import PriceCriteria
from RatingCriteria import RatingCriteria

app = FastAPI()


class CourseExploration:
    _db = None

    def __init__(self):
        try:
            DATABASE_URL = "mongodb+srv://admin:admin@courses.2nficpj.mongodb.net/?retryWrites=true&w=majority"
            client = MongoClient(DATABASE_URL)
            CourseExploration._db = client["courses_db"]
        except Exception as e:
            print(e)

    @staticmethod
    def get_courses(search: str = None, platform: str = None):
        course_exploration = CourseExploration()
        courses_collection = CourseExploration._db["courses"]
        courses = list(courses_collection.find())

        print(search)
        if search:
            courses = [c for c in courses if
                       search.strip().lower() in c["title"].lower() or search in c["description"].lower()]
        print(platform)
        if platform:
            courses = [c for c in courses if platform.strip().lower() == c["platform"].lower()]

        print(courses)

        for c in courses:
            c["_id"] = str(c["_id"])
            c["id"] = str(c["_id"])

        print(courses)

        return courses

    @staticmethod
    def get_filtered_courses(filter, filter_value):
        course_exploration = CourseExploration()
        courses_collection = CourseExploration._db["courses"]
        courses = list(courses_collection.find())

        if filter == "platform":
            filter_criteria = PlatformCriteria(filter_value)
            courses = [c for c in courses if filter_criteria.meetsCriteria(c)]
        elif filter == "level":
            filter_criteria = LevelCriteria(filter_value)
            courses = [c for c in courses if filter_criteria.meetsCriteria(c)]
        elif filter == "price":
            filter_criteria = PriceCriteria(float(filter_value))
            courses = [c for c in courses if filter_criteria.meetsCriteria(c)]
        else: # avg_rating
            url = f"http://localhost:8001/reviews/average_ratings"
            response = requests.get(url)
            temp_courses = None
            if response.status_code == 200:
                temp_courses = response.json()
            filter_criteria = RatingCriteria(float(filter_value))
            temp_courses = [c for c in temp_courses if filter_criteria.meetsCriteria(c)]
            print(temp_courses)
            print(courses)
            courses = [c for c in courses for tc in temp_courses if str(c["_id"]) == tc["_id"]]

        for c in courses:
            c["_id"] = str(c["_id"])
            c["id"] = str(c["_id"])

        print(courses)

        return courses

    @staticmethod
    def get_course(course_id: str):
        course_exploration = CourseExploration()
        courses_collection = CourseExploration._db["courses"]

        # Find the course with the specified ID (convert ID to ObjectId)
        course = courses_collection.find_one({"_id": ObjectId(course_id)})

        # Check if course was found
        if not course:
            return {"message": f"Course with ID {course_id} not found"}

        course["id"] = str(course["_id"])

        return course


@app.get("/courses", response_model=list[Course])
def get_courses(search: str = None, platform: str = None):
    return CourseExploration.get_courses(search, platform)


@app.get("/courses/filter", response_model=list[Course])
def get_filtered_courses(filter, filter_value):
    return CourseExploration.get_filtered_courses(filter, filter_value)


@app.get("/courses/{course_id}", response_model=Course)
def get_course(course_id: str):
    return CourseExploration.get_course(course_id)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("course_exploration_subsystem:app", host="0.0.0.0", port=8000)
