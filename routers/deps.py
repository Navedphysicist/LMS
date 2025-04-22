from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from db.database import get_db
from models.user import DbUser
import uuid

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> DbUser:
    # In a real application, you would verify the JWT token here
    # For this example, we'll just return a mock user
    user = db.query(DbUser).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
