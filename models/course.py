from sqlalchemy import Column, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base
from models.enrollments import enrollments


class DbCourse(Base):
    __tablename__ = 'courses'

    id = Column(String, primary_key=True)
    title = Column(String(255), nullable=False)
    category = Column(String(100))
    level = Column(String(50))
    primary_language = Column(String(50))
    subtitle = Column(String(255))
    description = Column(Text)
    image = Column(String(255))
    welcome_message = Column(Text)
    pricing = Column(Float)
    revenue = Column(Float, default=0.0)
    instructor_name = Column(String(100))

    # Foreign Keys
    instructor_id = Column(String, ForeignKey('users.id'))

    # Relationships
    instructor = relationship("DbUser", back_populates="created_courses")
    curriculum = relationship("DbCurrItem", back_populates="course")
    students = relationship(
        "DbUser",
        secondary=enrollments,
        back_populates="enrolled_courses"
    )
