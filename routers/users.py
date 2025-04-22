from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from db.database import get_db
from models.user import DbUser
from schemas.base_schema import UserResponse
from routers.deps import get_current_user
import uuid

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
async def get_user_profile(
    current_user: DbUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_user_profile(
    name: str,
    bio: str = None,
    avatar: UploadFile = File(None),
    current_user: DbUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    current_user.name = name
    if bio:
        current_user.bio = bio

    if avatar:
        # In a real application, you would save the file and store its path
        current_user.avatar = f"avatars/{uuid.uuid4()}.jpg"

    db.commit()
    db.refresh(current_user)
    return current_user
