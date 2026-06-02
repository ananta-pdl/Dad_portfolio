from pydantic import BaseModel, Field
from typing import Optional

class MusicBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=150)
    year: Optional[int] = Field(None, ge=1900, le=2100)
    description: Optional[str] = Field(None, max_length=500)
    audio_url: str = Field(..., description="Cloudinary direct audio link")
    cover_image_url: Optional[str] = Field(None, description="Cloudinary album cover image link")
    order: int = Field(0, description="Display order of the track")

class MusicCreate(MusicBase):
    pass

class MusicResponse(MusicBase):
    id: str
