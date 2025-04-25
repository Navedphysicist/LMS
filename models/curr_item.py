from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base


class DbCurrItem(Base):
    __tablename__ = 'curriculum_items'

    id = Column(String, primary_key=True)
    title = Column(String(255), nullable=False)
    video_url = Column(String(255))
    public_id = Column(String(255))
    is_free_preview = Column(Boolean, default=False)

    # Foreign Keys
    course_id = Column(String, ForeignKey('courses.id'))

    # Relationships
    course = relationship("DbCourse", back_populates="curriculum")
