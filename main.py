from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.database import engine, Base
from models.user import DbUser
from models.course import DbCourse
from models.curr_item import DbCurrItem
from routers import users, courses, auth

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LMS API",
    description="Learning Management System API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(courses.router)


@app.get("/")
async def root():
    return {"message": "Welcome to LMS API"}
