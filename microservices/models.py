from pydantic import BaseModel


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


class Progress(BaseModel):
    user_id: str
    course_id: str
    completion_status: str
    progress_details: dict


class PaymentData(BaseModel):
    user_id: str
    course_id: str
    payment_method: str
