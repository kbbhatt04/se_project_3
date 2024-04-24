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