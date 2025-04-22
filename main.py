from fastapi import FastAPI
from db.database import engine, Base
from models.user import DbUser
from models.course import DbCourse
from models.curr_item import DbCurrItem
from routers import users, courses

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LMS API",
    description="Learning Management System API",
    version="1.0.0"
)

# Include routers
app.include_router(users.router)
app.include_router(courses.router)


@app.get("/")
async def root():
    return {"message": "Welcome to LMS API"}
