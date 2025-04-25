from sqlalchemy.orm import Session
from models.user import DbUser
from models.course import DbCourse
from models.curr_item import DbCurrItem
from schemas.base_schema import UserCreate, CourseCreate
from services.auth import get_password_hash
from data.seed_data import INSTRUCTORS, STUDENTS, COURSES
import uuid


def create_user(db: Session, user_data: dict) -> DbUser:
    """Create a new user with hashed password"""
    user_create = UserCreate(
        name=user_data["name"],
        email=user_data["email"],
        password=user_data["password"],
        bio=user_data["bio"],
        avatar=user_data["avatar"]
    )

    db_user = DbUser(
        id=str(uuid.uuid4()),
        name=user_create.name,
        email=user_create.email,
        hashed_password=get_password_hash(user_create.password),
        bio=user_create.bio,
        avatar=user_create.avatar
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_course(db: Session, course_data: dict, instructor: DbUser) -> DbCourse:
    """Create a course with its curriculum items"""
    # Create the course
    course = DbCourse(
        id=course_data["id"],
        title=course_data["title"],
        category=course_data["category"],
        level=course_data["level"],
        primary_language=course_data["primary_language"],
        subtitle=course_data["subtitle"],
        description=course_data["description"],
        image=course_data["image"],
        welcome_message=course_data["welcome_message"],
        pricing=course_data["pricing"],
        instructor_id=instructor.id,
        instructor_name=instructor.name,
        objectives=course_data["objectives"]
    )

    db.add(course)
    db.commit()
    db.refresh(course)

    # Create curriculum items
    for item in course_data["curriculum"]:
        curr_item = DbCurrItem(
            id=item["id"],
            title=item["title"],
            video_url=item["video_url"],
            public_id=item["public_id"],
            is_free_preview=item["is_free_preview"],
            course_id=course.id
        )
        db.add(curr_item)

    db.commit()
    db.refresh(course)
    return course


def seed_database(db: Session):
    """Seed the database with initial data"""
    # Create instructors
    instructors = {}
    for instructor_data in INSTRUCTORS:
        instructor = create_user(db, instructor_data)
        instructors[instructor.name] = instructor

    # Create courses
    for course_data in COURSES:
        instructor = instructors[course_data["instructor_name"]]
        create_course(db, course_data, instructor)

    # Create students and enroll them in courses
    students = []
    for student_data in STUDENTS:
        student = create_user(db, student_data)
        students.append(student)

    # Enroll students in courses
    courses = db.query(DbCourse).all()
    for student in students:
        for course in courses[:2]:  # Enroll each student in first two courses
            student.enrolled_courses.append(course)

    db.commit()
