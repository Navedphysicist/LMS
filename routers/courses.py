from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from db.database import get_db
from models.user import DbUser
from models.course import DbCourse
from models.curr_item import DbCurrItem
from schemas.base_schema import CourseResponse
from routers.auth import get_current_user
from utils.cloud_utils import upload_image_to_cloudinary
import uuid
import json

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("", response_model=List[CourseResponse])
def get_courses(
    level: Optional[str] = None,
    price_min: Optional[float] = Query(None, alias="priceMin"),
    price_max: Optional[float] = Query(None, alias="priceMax"),
    language: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(DbCourse)

    if level:
        query = query.filter(DbCourse.level.ilike(level))
    if price_min is not None:
        query = query.filter(DbCourse.pricing >= price_min)
    if price_max is not None:
        query = query.filter(DbCourse.pricing <= price_max)
    if language:
        query = query.filter(DbCourse.primary_language.ilike(language))
    if category:
        query = query.filter(DbCourse.category.ilike(category))

    return query.all()


@router.post("", response_model=CourseResponse)
def create_course(
    course_data: str = Form(...),  # JSON string containing course details
    image: UploadFile = File(None),  # Optional image file
    current_user: DbUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Parse the JSON data
        data = json.loads(course_data)
        course_id = str(uuid.uuid4())

        image_url = ""
        if image:
            try:
                image_url = upload_image_to_cloudinary(
                    file=image,
                    folder="lms/courses",
                    public_id=f"course_{course_id}_cover"
                )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Image upload failed: {str(e)}"
                )

        db_course = DbCourse(
            id=course_id,
            title=data["title"],
            category=data["category"],
            level=data["level"],
            primary_language=data["primaryLanguage"],
            subtitle=data["subtitle"],
            description=data["description"],
            welcome_message=data["welcomeMessage"],
            pricing=data["pricing"],
            image=image_url,
            objectives=data.get("objectives", []),
            instructor_id=current_user.id,
            instructor_name=current_user.name
        )
        db.add(db_course)
        db.commit()
        db.refresh(db_course)

        # Create curriculum items
        for item in data.get("curriculum", []):
            curr_item = DbCurrItem(
                id=str(uuid.uuid4()),
                title=item["title"],
                video_url=item.get("video_url"),
                public_id=item.get("public_id"),
                is_free_preview=item.get("is_free_preview", False),
                course_id=db_course.id
            )
            db.add(curr_item)

        db.commit()
        db.refresh(db_course)
        return db_course
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/my-courses", response_model=List[CourseResponse])
def get_my_courses(
    current_user: DbUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(DbCourse).filter(DbCourse.instructor_id == current_user.id).all()


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(
    course_id: str,
    current_user: DbUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    course = db.query(DbCourse).filter(
        DbCourse.id == course_id,
        DbCourse.instructor_id == current_user.id
    ).first()

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    db.delete(course)
    db.commit()
    return {"message": "Course deleted successfully"}


# Extra routes for the enrolled courses


@router.post("/{course_id}/enroll", status_code=status.HTTP_201_CREATED)
def enroll_in_course(
    course_id: str,
    current_user: DbUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    course = db.query(DbCourse).filter(DbCourse.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    # Check if already enrolled
    if course in current_user.enrolled_courses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are already enrolled in this course"
        )

    current_user.enrolled_courses.append(course)
    db.commit()
    db.refresh(current_user)
    return {"message": f"You have enrolled in {course.title} successfully"}


@router.get("/enrolled-courses", response_model=List[CourseResponse])
def get_enrolled_courses(
    current_user: DbUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return current_user.enrolled_courses
