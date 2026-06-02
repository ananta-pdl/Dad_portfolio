from fastapi import APIRouter, HTTPException
from app.models.music import MusicResponse, MusicCreate
from app.database import get_db
from app.services.cloudinary import get_resources_by_folder_robust
from app.config import settings
import logging
import uuid
from typing import Optional

logger = logging.getLogger("uvicorn")
router = APIRouter(prefix="/api/music", tags=["Music"])

# Pre-seeded mock songs (using public royalty-free MP3s so they play successfully)
DEFAULT_SONGS = [
    {
        "id": "track-1",
        "title": "Melodies of the Autumn Wind",
        "year": 1982,
        "description": "A soulful acoustic ballad recorded live in a student radio studio. Features raw acoustic guitar and emotional vocals.",
        "audio_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
        "cover_image_url": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=500&q=80",
        "order": 1
    },
    {
        "id": "track-2",
        "title": "Midnight Jazz Reflections",
        "year": 1985,
        "description": "Late-night jam session in a cozy jazz bar. Smooth saxophone melodies layered with piano chord structures.",
        "audio_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
        "cover_image_url": "https://images.unsplash.com/photo-1487180142328-0c4e37023af5?w=500&q=80",
        "order": 2
    },
    {
        "id": "track-3",
        "title": "Chasing Shadows (Synth Wave)",
        "year": 1988,
        "description": "A synth-pop experiment showcasing early electronic keyboard arrangements, drum machines, and futuristic vibes.",
        "audio_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
        "cover_image_url": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=500&q=80",
        "order": 3
    },
    {
        "id": "track-4",
        "title": "Harmonies of Tomorrow",
        "year": 1991,
        "description": "A final studio recording celebrating friendship and new beginnings before transitioning fully to a corporate career.",
        "audio_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3",
        "cover_image_url": "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=500&q=80",
        "order": 4
    }
]

CLOUDINARY_TRACKS_META = {
    "Okhaldhungaima__1_ythiv9": {
        "title": "Okhaldhungaima - Part 1",
        "year": 1983,
        "description": "A soulful recording of the classic ballad 'Okhaldhungaima', capturing stories of the hills and the beauty of home. Vocals and acoustic guitar by Gandharba Raj Paudel.",
        "cover_image_url": "https://res.cloudinary.com/ducdlgkcq/image/upload/v1780375240/baba_pic_lmk02i.jpg",
        "order": 1
    },
    "music1_ew7zws": {
        "title": "Nepali Folk Reflections (Acoustic Demo)",
        "year": 1985,
        "description": "An acoustic guitar demo exploring traditional rhythms merged with contemporary folk melodies.",
        "cover_image_url": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=500&q=80",
        "order": 2
    },
    "music2_ni2ed1": {
        "title": "Autumn Melodies (Live Cassette)",
        "year": 1988,
        "description": "Live recording preserved from a community studio session, featuring raw acoustic guitar and expressive vocals.",
        "cover_image_url": "https://images.unsplash.com/photo-1487180142328-0c4e37023af5?w=500&q=80",
        "order": 3
    },
    "Okhaldhungaima__3_qrcia6": {
        "title": "Okhaldhungaima - Part 3",
        "year": 1983,
        "description": "Acoustic fingerpicking variation of the classic Nepalese folk melody, showing detailed guitar arrangements.",
        "cover_image_url": "https://res.cloudinary.com/ducdlgkcq/image/upload/v1780375240/baba_pic_lmk02i.jpg",
        "order": 4
    },
    "Okhaldhungaima__4_bprg8m": {
        "title": "Okhaldhungaima - Part 4 (Studio Outtake)",
        "year": 1984,
        "description": "A vintage studio outtake recording with warm vocal harmonies and acoustic instrumentation.",
        "cover_image_url": "https://res.cloudinary.com/ducdlgkcq/image/upload/v1780375240/baba_pic_lmk02i.jpg",
        "order": 5
    }
}

def map_cloudinary_track(resource, index) -> MusicResponse:
    public_id = resource.get("public_id", "")
    filename = public_id.split("/")[-1]
    
    meta = CLOUDINARY_TRACKS_META.get(filename)
    if meta:
        return MusicResponse(
            id=resource.get("asset_id", str(uuid.uuid4())),
            title=meta["title"],
            year=meta["year"],
            description=meta["description"],
            audio_url=resource.get("secure_url"),
            cover_image_url=meta["cover_image_url"],
            order=meta["order"]
        )
    
    # Generic fallback cleaner
    clean_title = filename.replace("_", " ").replace("-", " ").title()
    # Strip random hash suffixes if present
    parts = clean_title.split()
    if len(parts) > 1 and len(parts[-1]) >= 6 and parts[-1].lower().isalnum():
        clean_title = " ".join(parts[:-1])
        
    return MusicResponse(
        id=resource.get("asset_id", str(uuid.uuid4())),
        title=clean_title,
        year=2026,
        description="A beautiful musical composition uploaded to Cloudinary.",
        audio_url=resource.get("secure_url"),
        cover_image_url="https://res.cloudinary.com/ducdlgkcq/image/upload/v1780375240/baba_pic_lmk02i.jpg",
        order=index + 10
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
            # Sort by order
            mapped_tracks.sort(key=lambda t: t.order)
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
        
    # Priority 3: Return pre-seeded defaults
    logger.info("Returning default pre-seeded tracks.")
    return [MusicResponse(**song) for song in DEFAULT_SONGS]

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
