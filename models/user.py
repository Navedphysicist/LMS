from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from db.database import Base
from models.enrollments import enrollments


class DbUser(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    bio = Column(Text)
    avatar = Column(String(255))

    # Relationships
    created_courses = relationship("DbCourse", back_populates="instructor")
    enrolled_courses = relationship(
        "DbCourse",
        secondary=enrollments,
        back_populates="students"
    )
