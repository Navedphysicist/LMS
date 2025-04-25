import cloudinary
import cloudinary.uploader
from fastapi import UploadFile, HTTPException, status
from config import get_settings
import uuid

settings = get_settings()
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)



def upload_image_to_cloudinary(file: UploadFile, folder: str, public_id: str = None) -> str:

    if file.content_type not in {"image/jpeg", "image/png", "image/webp", "image/gif"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only JPEG, PNG, WebP, and GIF formats are allowed."
        )

    try:
        public_id = f"{folder}/{uuid.uuid4()}"
        result = cloudinary.uploader.upload(
            file.file,
            public_id=public_id,
            folder=folder,
            overwrite=True,
            resource_type="image"
        )
        return result["secure_url"]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Cloudinary upload failed: {str(e)}"
        )


def upload_avatar_to_cloudinary(file: UploadFile, public_id: str = None) -> str:

    return upload_image_to_cloudinary(file, "lms/avatars", public_id)


def upload_course_image_to_cloudinary(file: UploadFile, public_id: str = None) -> str:

    return upload_image_to_cloudinary(file, "lms/courses", public_id)
