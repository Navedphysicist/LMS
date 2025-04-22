from sqlalchemy import Table, Column, String, ForeignKey
from db.database import Base

enrollments = Table(
    'enrollments',
    Base.metadata,
    Column('user_id', String, ForeignKey('users.id'), primary_key=True),
    Column('course_id', String, ForeignKey('courses.id'), primary_key=True)
)
