from __future__ import annotations
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from schemas.curr_item import CurrItemResponse

# User Models


class UserBase(BaseModel):
    name: str
    email: EmailStr
    bio: Optional[str] = None
    avatar: Optional[str] = None

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    name:str
    email: EmailStr
    password: str


class UserBasicInfo(UserBase):
    id: str

    class Config:
        from_attributes = True

# Course Models


class CourseBase(BaseModel):
    title: str
    category: Optional[str] = None
    level: Optional[str] = None
    primary_language: Optional[str] = None
    subtitle: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    welcome_message: Optional[str] = None
    pricing: float = Field(ge=0)
    instructor_name: str
    objectives: List[str] = []
    curriculum: List[CurrItemResponse] = []

    class Config:
        from_attributes = True


class CourseCreate(CourseBase):
    pass


class CourseBasicInfo(CourseBase):
    id: str
    revenue: float = 0.0

    class Config:
        from_attributes = True

# Response Models


class UserResponse(UserBase):
    id: str
    created_courses: List[CourseBasicInfo] = []
    enrolled_courses: List[CourseBasicInfo] = []

    class Config:
        from_attributes = True


class CourseResponse(CourseBase):
    id: str
    revenue: float = 0.0
    instructor: UserBasicInfo
    students: List[UserBasicInfo] = []

    class Config:
        from_attributes = True
