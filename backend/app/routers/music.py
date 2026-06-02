from fastapi import APIRouter, HTTPException
from app.models.music import MusicResponse, MusicCreate
from app.database import get_db
from app.services.cloudinary import get_resources_by_folder_robust
from app.config import settings
import logging
import uuid
from urllib.parse import quote

logger = logging.getLogger("uvicorn")
router = APIRouter(prefix="/api/music", tags=["Music"])

def cloudinary_video_thumbnail(public_id: str) -> str:
    encoded_public_id = quote(public_id, safe="/")
    return f"https://res.cloudinary.com/{settings.cloudinary_cloud_name}/video/upload/so_0/{encoded_public_id}.jpg"

def map_cloudinary_track(resource, index: int) -> MusicResponse:
    public_id = resource.get("public_id", "")
    return MusicResponse(
        id=resource.get("asset_id", str(uuid.uuid4())),
        title=f"Okhaldhungaima {index + 1}",
        year=None,
        description=None,
        audio_url=resource.get("secure_url"),
        cover_image_url=cloudinary_video_thumbnail(public_id) if public_id else None,
        order=index + 1
    )

@router.get("/", response_model=list[MusicResponse])
async def get_tracks():
    logger.info("Fetching music tracks...")
    
    # Priority 1: Fetch from Cloudinary
    try:
        cloudinary_resources = get_resources_by_folder_robust(settings.cloudinary_music_folder)
        if cloudinary_resources:
            logger.info(f"Loaded {len(cloudinary_resources)} music tracks from Cloudinary folder '{settings.cloudinary_music_folder}'")
            mapped_tracks = [map_cloudinary_track(res, idx) for idx, res in enumerate(cloudinary_resources)]
            return mapped_tracks
    except Exception as e:
        logger.warning(f"Failed to load music from Cloudinary folder ({e}). Trying database...")
        
    # Priority 2: Fetch from MongoDB
    tracks = []
    try:
        db = get_db()
        cursor = db.music.find().sort("order", 1)
        async for doc in cursor:
            tracks.append(
                MusicResponse(
                    id=str(doc["_id"]),
                    title=doc["title"],
                    year=doc.get("year"),
                    description=doc.get("description"),
                    audio_url=doc["audio_url"],
                    cover_image_url=doc.get("cover_image_url"),
                    order=doc["order"]
                )
            )
        
        if tracks:
            logger.info(f"Loaded {len(tracks)} music tracks from MongoDB.")
            return tracks
    except Exception as e:
        logger.warning(f"MongoDB connection failed for music router ({e}). Falling back to pre-seeded defaults.")
        
    logger.warning("No music tracks available from Cloudinary or MongoDB.")
    return []

@router.post("/", response_model=MusicResponse)
async def create_track(track_in: MusicCreate):
    try:
        db = get_db()
        track_id = str(uuid.uuid4())
        document = track_in.model_dump()
        document["_id"] = track_id
        
        await db.music.insert_one(document)
        logger.info(f"Created music track in DB: {track_in.title}")
        return MusicResponse(id=track_id, **track_in.model_dump())
    except Exception as e:
        logger.error(f"Failed to create track in MongoDB: {e}")
        raise HTTPException(status_code=500, detail="Database write operation failed.")
