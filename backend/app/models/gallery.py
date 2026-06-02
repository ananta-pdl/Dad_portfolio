from pydantic import BaseModel, Field
from typing import Optional

class GalleryBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=150)
    description: Optional[str] = Field(None, max_length=1000)
    image_url: str = Field(..., description="Cloudinary direct image link")
    date: Optional[str] = Field(None, description="Date of achievement (e.g., '1985' or 'June 2024')")
    category: str = Field("corporate", description="Category: 'corporate', 'music', 'personal'")

class GalleryCreate(GalleryBase):
    pass

class GalleryResponse(GalleryBase):
    id: str
