import requests

SERVER_URL = "http://localhost:8000"


def get_courses():
    response = requests.get(f"{SERVER_URL}/courses")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error getting courses: {response.text}")
        return None


def enroll_course(course_id, user_id):
    data = {"course_id": course_id, "user_id": user_id}
    response = requests.post(f"{SERVER_URL}/enroll?course_id={course_id}&user_id={user_id}",
                             json=data)
    if response.status_code == 200:
        print((response.json()))
    else:
        print(f"Error enrolling course: {response.text}")


def add_review(course_id, user_id, rating, review):
    response = requests.post(
        f"{SERVER_URL}/add_review",
        json={"user_id": user_id, "course_id": course_id, "rating": rating, "review": review}
    )
    if response.status_code == 200:
        print(response.json()["message"])
    else:
        print(f"Error submitting review: {response.status_code}")


courses = get_courses()
if courses:
    for course in courses:
        print(f"{course['id']}")
    course_id = input("Enter id of the course you want to enroll for: ")
    user_id = input("Enter your user id: ")
    enroll_course(course_id, user_id)

    rating = int(input("Give a rating on scale of 1 to 5: "))
    review = input("Write a review for the course: ")
    add_review(course_id, user_id, rating, review)
