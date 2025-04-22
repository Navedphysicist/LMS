from sqlalchemy.orm import Session
from db.database import engine, Base, get_db
from models.user import DbUser
from models.course import DbCourse
from models.curr_item import DbCurrItem
from schemas.base_schema import UserCreate, CourseCreate
import uuid

# Create all tables
Base.metadata.create_all(bind=engine)


def seed_database():
    db = next(get_db())

    # Create instructors
    instructors = {
        "John Doe": create_user(db, UserCreate(
            name="John Doe",
            email="john@example.com",
            password="password123",
            bio="Experienced instructor specializing in technology education.",
            avatar=f"https://ui-avatars.com/api/?name=John+Doe"
        )),
        "Jane Smith": create_user(db, UserCreate(
            name="Jane Smith",
            email="jane@example.com",
            password="password123",
            bio="Experienced instructor specializing in technology education.",
            avatar=f"https://ui-avatars.com/api/?name=Jane+Smith"
        )),
        "Mark Lee": create_user(db, UserCreate(
            name="Mark Lee",
            email="mark@example.com",
            password="password123",
            bio="Experienced instructor specializing in technology education.",
            avatar=f"https://ui-avatars.com/api/?name=Mark+Lee"
        )),
        "Sophia Green": create_user(db, UserCreate(
            name="Sophia Green",
            email="sophia@example.com",
            password="password123",
            bio="Experienced instructor specializing in technology education.",
            avatar=f"https://ui-avatars.com/api/?name=Sophia+Green"
        ))
    }

    # Course data
    courses_data = [
        {
            "id": "674ee4382b93b83f879600f3",
            "title": "Full Stack Development Bootcamp",
            "category": "Technology",
            "level": "Beginner",
            "primary_language": "English",
            "subtitle": "Learn the basics of web development",
            "description": "The Full Stack Development Bootcamp is a comprehensive and hands-on course designed to equip you with the essential skills and knowledge required to become a professional full-stack developer...",
            "image": "http://res.cloudinary.com/doibocmzz/image/upload/v1733270810/j932bfxuytfjzubck8m.webp",
            "welcome_message": "Welcome to the Full Stack Development Bootcamp!",
            "pricing": 200,
            "instructor_name": "John Doe",
            "curriculum": [
                {
                    "title": "Introduction to HTML",
                    "video_url": "http://res.cloudinary.com/doibocmzz/video/upload/v1733223391/yyrsqwfxuytfjzubck8m.mp4",
                    "public_id": "yyrsqwfxuytfjzubck8m",
                    "is_free_preview": True
                }
            ]
        },
        {
            "id": "674ee56e2b93b83f879600f6",
            "title": "Frontend Development with React",
            "category": "Technology",
            "level": "Intermediate",
            "primary_language": "English",
            "subtitle": "Master modern frontend development with React",
            "description": "Dive into React and learn how to build interactive user interfaces.",
            "image": "http://res.cloudinary.com/doibocmzz/image/upload/v1733270810/j932bfxa0kcrynbabdlf.webp",
            "welcome_message": "Welcome to the React Frontend Development Course!",
            "pricing": 150,
            "instructor_name": "Jane Smith",
            "curriculum": [
                {
                    "title": "Getting Started with React",
                    "video_url": "http://res.cloudinary.com/doibocmzz/video/upload/v1733223391/yyrsqwfxuytfjzubck8m.mp4",
                    "public_id": "yyrsqwfxuytfjzubck8m",
                    "is_free_preview": True
                }
            ]
        },
        {
            "id": "674ee8502b93b83f879600f9",
            "title": "Backend Development with Node.js",
            "category": "Technology",
            "level": "Advanced",
            "primary_language": "English",
            "subtitle": "Build server-side applications with Node.js",
            "description": "Learn how to create robust backend services using Node.js.",
            "image": "http://res.cloudinary.com/doibocmzz/image/upload/v1733270810/j932bfxa0kcrynbabdlf.webp",
            "welcome_message": "Welcome to the Node.js Backend Development Course!",
            "pricing": 250,
            "instructor_name": "Mark Lee",
            "curriculum": [
                {
                    "title": "Node.js Basics",
                    "video_url": "http://res.cloudinary.com/doibocmzz/video/upload/v1733223391/yyrsqwfxuytfjzubck8m.mp4",
                    "public_id": "yyrsqwfxuytfjzubck8m",
                    "is_free_preview": True
                }
            ]
        },
        {
            "id": "674f9d1e065060a46096c9d1",
            "title": "Introduction to Generative AI",
            "category": "Technology",
            "level": "Beginner",
            "primary_language": "English",
            "subtitle": "Understand and build generative AI models",
            "description": "A beginner-friendly course to explore the basics of Generative AI and its applications.",
            "image": "http://res.cloudinary.com/doibocmzz/image/upload/v1733270810/j932bfxa0kcrynbabdlf.webp",
            "welcome_message": "Welcome to the Generative AI Course!",
            "pricing": 300,
            "instructor_name": "Sophia Green",
            "curriculum": [
                {
                    "title": "What is Generative AI?",
                    "video_url": "http://res.cloudinary.com/doibocmzz/video/upload/v1733223391/yyrsqwfxuytfjzubck8m.mp4",
                    "public_id": "yyrsqwfxuytfjzubck8m",
                    "is_free_preview": True
                }
            ]
        },
        {
            "id": "674ff0012b93b83f87960101",
            "title": "DevOps Essentials",
            "category": "Technology",
            "level": "Intermediate",
            "primary_language": "English",
            "subtitle": "Learn the foundations of DevOps",
            "description": "A hands-on course to understand and implement DevOps practices.",
            "image": "http://res.cloudinary.com/doibocmzz/image/upload/v1733270810/j932bfxa0kcrynbabdlf.webp",
            "welcome_message": "Welcome to the DevOps Essentials Course!",
            "pricing": 200,
            "instructor_name": "Mark Lee",
            "curriculum": [
                {
                    "title": "Introduction to DevOps",
                    "video_url": "http://res.cloudinary.com/doibocmzz/video/upload/v1733223391/devops_intro.mp4",
                    "public_id": "devops_intro",
                    "is_free_preview": True
                },
                {
                    "title": "Version Control with Git",
                    "video_url": "http://res.cloudinary.com/doibocmzz/video/upload/v1733223391/git_version_control.mp4",
                    "public_id": "git_version_control",
                    "is_free_preview": False
                },
                {
                    "title": "Continuous Integration (CI)",
                    "video_url": "http://res.cloudinary.com/doibocmzz/video/upload/v1733223391/ci_pipelines.mp4",
                    "public_id": "ci_pipelines",
                    "is_free_preview": False
                }
            ]
        },
        {
            "id": "674ff0102b93b83f87960107",
            "title": "Cloud Computing with AWS",
            "category": "Technology",
            "level": "Advanced",
            "primary_language": "English",
            "subtitle": "Master AWS cloud services",
            "description": "Learn how to design and deploy applications on AWS cloud.",
            "image": "http://res.cloudinary.com/doibocmzz/image/upload/v1733270810/j932bfxa0kcrynbabdlf.webp",
            "welcome_message": "Welcome to the Cloud Computing with AWS Course!",
            "pricing": 250,
            "instructor_name": "Mark Lee",
            "curriculum": [
                {
                    "title": "Introduction to Cloud Computing",
                    "video_url": "http://res.cloudinary.com/doibocmzz/video/upload/v1733223391/cloud_intro.mp4",
                    "public_id": "cloud_intro",
                    "is_free_preview": True
                },
                {
                    "title": "AWS EC2 Basics",
                    "video_url": "http://res.cloudinary.com/doibocmzz/video/upload/v1733223391/aws_ec2_basics.mp4",
                    "public_id": "aws_ec2_basics",
                    "is_free_preview": False
                }
            ]
        },
        {
            "id": "674ff0202b93b83f87960113",
            "title": "Agile Project Management",
            "category": "Business",
            "level": "Beginner",
            "primary_language": "English",
            "subtitle": "A practical guide to Agile methodologies",
            "description": "Understand and implement Agile practices for project management.",
            "image": "http://res.cloudinary.com/doibocmzz/image/upload/v1733270810/j932bfxa0kcrynbabdlf.webp",
            "welcome_message": "Welcome to the Agile Project Management Course!",
            "pricing": 180,
            "instructor_name": "Jane Smith",
            "curriculum": [
                {
                    "title": "Introduction to Agile",
                    "video_url": "http://res.cloudinary.com/doibocmzz/video/upload/v1733223391/agile_intro.mp4",
                    "public_id": "agile_intro",
                    "is_free_preview": True
                },
                {
                    "title": "Scrum Basics",
                    "video_url": "http://res.cloudinary.com/doibocmzz/video/upload/v1733223391/scrum_basics.mp4",
                    "public_id": "scrum_basics",
                    "is_free_preview": True
                }
            ]
        },
        {
            "id": "674ff0302b93b83f87960119",
            "title": "Data Structures and Algorithms",
            "category": "Technology",
            "level": "Advanced",
            "primary_language": "English",
            "subtitle": "Master problem-solving skills",
            "description": "Learn essential data structures and algorithms to crack coding interviews.",
            "image": "http://res.cloudinary.com/doibocmzz/image/upload/v1733270810/j932bfxa0kcrynbabdlf.webp",
            "welcome_message": "Welcome to the Data Structures and Algorithms Course!",
            "pricing": 300,
            "instructor_name": "John Doe",
            "curriculum": [
                {
                    "title": "Introduction to Algorithms",
                    "video_url": "http://res.cloudinary.com/doibocmzz/video/upload/v1733223391/algorithms_intro.mp4",
                    "public_id": "algorithms_intro",
                    "is_free_preview": True
                },
                {
                    "title": "Arrays and Strings",
                    "video_url": "http://res.cloudinary.com/doibocmzz/video/upload/v1733223391/arrays_strings.mp4",
                    "public_id": "arrays_strings",
                    "is_free_preview": False
                }
            ]
        },
        {
            "id": "674ff0402b93b83f87960125",
            "title": "Cybersecurity Fundamentals",
            "category": "Technology",
            "level": "Beginner",
            "primary_language": "English",
            "subtitle": "Protect systems and data",
            "description": "A beginner's guide to understanding cybersecurity principles.",
            "image": "http://res.cloudinary.com/doibocmzz/image/upload/v1733270810/j932bfxa0kcrynbabdlf.webp",
            "welcome_message": "Welcome to the Cybersecurity Fundamentals Course!",
            "pricing": 200,
            "instructor_name": "Sophia Green",
            "curriculum": [
                {
                    "title": "Introduction to Cybersecurity",
                    "video_url": "http://res.cloudinary.com/doibocmzz/video/upload/v1733223391/cyber_intro.mp4",
                    "public_id": "cyber_intro",
                    "is_free_preview": True
                },
                {
                    "title": "Understanding Network Security",
                    "video_url": "http://res.cloudinary.com/doibocmzz/video/upload/v1733223391/network_security.mp4",
                    "public_id": "network_security",
                    "is_free_preview": True
                }
            ]
        }
    ]

    # Create courses and their curriculum items
    for course_data in courses_data:
        instructor = instructors[course_data["instructor_name"]]
        course_create = CourseCreate(
            title=course_data["title"],
            category=course_data["category"],
            level=course_data["level"],
            primary_language=course_data["primary_language"],
            subtitle=course_data["subtitle"],
            description=course_data["description"],
            image=course_data["image"],
            welcome_message=course_data["welcome_message"],
            pricing=course_data["pricing"],
            instructor_name=course_data["instructor_name"]
        )
        course = create_course(db, course_create, instructor)

        # Create curriculum items
        for item_data in course_data["curriculum"]:
            curr_item = DbCurrItem(
                id=str(uuid.uuid4()),
                title=item_data["title"],
                video_url=item_data["video_url"],
                public_id=item_data["public_id"],
                is_free_preview=item_data["is_free_preview"],
                course_id=course.id
            )
            db.add(curr_item)
        db.commit()

    # Create students and enroll them in courses
    students = [
        create_user(db, UserCreate(
            name="Student One",
            email="student1@example.com",
            password="password123",
            bio="Eager learner",
            avatar=f"https://ui-avatars.com/api/?name=Student+One"
        )),
        create_user(db, UserCreate(
            name="Student Two",
            email="student2@example.com",
            password="password123",
            bio="Eager learner",
            avatar=f"https://ui-avatars.com/api/?name=Student+Two"
        ))
    ]

    # Enroll students in courses
    courses = db.query(DbCourse).all()
    for student in students:
        for course in courses[:2]:  # Enroll each student in first two courses
            student.enrolled_courses.append(course)
    db.commit()


def create_user(db: Session, user_create: UserCreate) -> DbUser:
    """Create a new user using the UserCreate schema"""
    db_user = DbUser(
        id=str(uuid.uuid4()),
        name=user_create.name,
        email=user_create.email,
        hashed_password=user_create.password,  # In production, this should be hashed
        bio=user_create.bio,
        avatar=user_create.avatar
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_course(db: Session, course_create: CourseCreate, instructor: DbUser) -> DbCourse:
    """Create a new course using the CourseCreate schema"""
    db_course = DbCourse(
        id=str(uuid.uuid4()),
        **course_create.model_dump(),
        instructor_id=instructor.id
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


if __name__ == "__main__":
    print("Seeding database...")
    seed_database()
    print("Database seeded successfully!")