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
    response = requests.post(f"{SERVER_URL}/enrollments/{course_id}?course_id={course_id}&&user_id={user_id}", json=data)
    if response.status_code == 200:
        print((response.json()))
    else:
        print(f"Error enrolling course: {response.text}")


courses = get_courses()
if courses:
    for course in courses:
        print(f"{course['id']}")
    course_id = input("Enter id of the course you want to enroll for: ")
    user_id = input("Enter your user id: ")
    enroll_course(course_id, user_id)