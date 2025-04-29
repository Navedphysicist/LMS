from __future__ import annotations
from pydantic import BaseModel
from typing import Optional


class CurrItemBase(BaseModel):
    title: str
    video_url: Optional[str] = None
    public_id: Optional[str] = None
    is_free_preview: bool = False

    class Config:
        from_attributes = True


class CurrItemCreate(CurrItemBase):
    course_id: str


class CurrItemResponse(CurrItemBase):
    id: str
    course_id: str
    
    class Config:
        from_attributes = True
