from fastapi import APIRouter, Depends, HTTPException, status, Response, Body, Header
from sqlalchemy.orm import Session
from db.database import get_db
from services.auth import authenticate_user, get_password_hash
from schemas.base_schema import UserCreate, UserResponse
from models.user import DbUser
from typing import Optional
import uuid

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(DbUser).filter(
        DbUser.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_password = get_password_hash(user_data.password)

    new_user = DbUser(
        id=str(uuid.uuid4()),
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_password,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login")
def login(
    response: Response,
    email: str = Body(...),
    password: str = Body(...),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, email, password)

    response.set_cookie(
        key="user_id",
        value=str(user.id),
        max_age=30
    )

    return {"message": f"Successfully logged in as {user.email}"}


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("user_id") 
    return {"message": "Successfully logged out"}


def get_current_user(
    user_id: Optional[str] = Header(None, alias="UserID"),
    db: Session = Depends(get_db)
):
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    user = db.query(DbUser).filter(DbUser.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user
