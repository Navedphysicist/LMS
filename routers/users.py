from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from db.database import get_db
from models.user import DbUser
from schemas.base_schema import UserResponse
from routers.auth import get_current_user
from utils.cloud_utils import upload_avatar_to_cloudinary
import uuid

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/my-profile", response_model=UserResponse)
async def get_user_profile(
    current_user: DbUser = Depends(get_current_user)):
    return current_user


@router.put("/my-profile", response_model=UserResponse)
def update_user_profile(
    name: str = Form(...),
    bio: str = Form(None),
    avatar: UploadFile = File(None),
    current_user: DbUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    current_user.name = name
    if bio:
        current_user.bio = bio

    if avatar:
        try:
            public_id = f"user_{current_user.id}_avatar"
            avatar_url = upload_avatar_to_cloudinary(avatar, public_id)
            current_user.avatar = avatar_url
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error processing avatar: {str(e)}"
            )
    db.commit()
    db.refresh(current_user)
    return current_user
