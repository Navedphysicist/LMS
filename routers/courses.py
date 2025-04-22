from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from db.database import get_db
from models.user import DbUser
from models.course import DbCourse
from models.enrollments import enrollments
from schemas.base_schema import CourseCreate, CourseResponse
from routers.deps import get_current_user
import uuid

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
        query = query.filter(DbCourse.level == level)
    if price_min is not None:
        query = query.filter(DbCourse.pricing >= price_min)
    if price_max is not None:
        query = query.filter(DbCourse.pricing <= price_max)
    if language:
        query = query.filter(DbCourse.primary_language == language)
    if category:
        query = query.filter(DbCourse.category == category)

    return query.all()


@router.post("", response_model=CourseResponse)
def create_course(
    course: CourseCreate,
    image: UploadFile = File(None),
    current_user: DbUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_course = DbCourse(
        id=str(uuid.uuid4()),
        **course.model_dump(),
        instructor_id=current_user.id
    )

    if image:
        # In a real application, you would save the file and store its path
        db_course.image = f"courses/{uuid.uuid4()}.jpg"

    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


@router.get("/my", response_model=List[CourseResponse])
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
            detail="Already enrolled in this course"
        )

    current_user.enrolled_courses.append(course)
    db.commit()


@router.get("/my-courses", response_model=List[CourseResponse])
def get_enrolled_courses(
    current_user: DbUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return current_user.enrolled_courses
