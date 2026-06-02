from fastapi import APIRouter, HTTPException
from app.models.gallery import GalleryResponse, GalleryCreate
from app.database import get_db
from app.services.cloudinary import get_resources_by_folder
import logging
import uuid
from typing import Optional

logger = logging.getLogger("uvicorn")
router = APIRouter(prefix="/api/gallery", tags=["Gallery"])

# Seeded achievements (Corporate & Music milestones)
DEFAULT_GALLERY = [
    {
        "id": "gal-1",
        "title": "Keynote Address at Global Tech Summit",
        "description": "Discussing business agility and innovation strategies at the annual executive leadership summit.",
        "image_url": "https://images.unsplash.com/photo-1475721027785-f74eccf877e2?w=800&q=80",
        "date": "October 2024",
        "category": "corporate"
    },
    {
        "id": "gal-2",
        "title": "First Studio Session with 'The Dreamers'",
        "description": "Recording vocals and guitar tracks for the debut demo cassette in a local community studio.",
        "image_url": "https://images.unsplash.com/photo-1598488035139-bdbb2231ce04?w=800&q=80",
        "date": "May 1983",
        "category": "music"
    },
    {
        "id": "gal-3",
        "title": "Recipient of Leadership Excellence Award",
        "description": "Honored by the Board of Directors for leading the company through a record-setting fiscal growth phase.",
        "image_url": "https://images.unsplash.com/photo-1578575437130-527eed3abbec?w=800&q=80",
        "date": "March 2021",
        "category": "corporate"
    },
    {
        "id": "gal-4",
        "title": "Reunion Live Show for Charity",
        "description": "Reuniting with old bandmates for a one-off performance, raising $50k for youth music education programs.",
        "image_url": "https://images.unsplash.com/photo-1465847899084-d164df4dedc6?w=800&q=80",
        "date": "December 2018",
        "category": "music"
    },
    {
        "id": "gal-5",
        "title": "Corporate Mentorship Launch",
        "description": "Introducing a new executive coaching curriculum for upcoming high-potential directors.",
        "image_url": "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=800&q=80",
        "date": "January 2025",
        "category": "corporate"
    },
    {
        "id": "gal-6",
        "title": "Acoustic Set at Retro Cafe",
        "description": "An intimate solo performance featuring covers of early folk classics and original ballads.",
        "image_url": "https://images.unsplash.com/photo-1459749411175-04bf5292ceea?w=800&q=80",
        "date": "August 1986",
        "category": "music"
    }
]

CLOUDINARY_GALLERY_META = {
    "baba_pic_lmk02i": {
        "title": "Gandharba Raj Paudel - Professional Portrait",
        "description": "Executive Director portrait reflecting a career of leadership, discipline, and creative expression.",
        "date": "June 2026",
        "category": "personal"
    }
}

def map_cloudinary_gallery(resource, index) -> GalleryResponse:
    public_id = resource.get("public_id", "")
    filename = public_id.split("/")[-1]
    
    meta = CLOUDINARY_GALLERY_META.get(filename)
    if meta:
        return GalleryResponse(
            id=resource.get("asset_id", str(uuid.uuid4())),
            title=meta["title"],
            description=meta["description"],
            image_url=resource.get("secure_url"),
            date=meta["date"],
            category=meta["category"]
        )
    
    # Generic fallback
    clean_title = filename.replace("_", " ").replace("-", " ").title()
    parts = clean_title.split()
    if len(parts) > 1 and len(parts[-1]) >= 6 and parts[-1].lower().isalnum():
        clean_title = " ".join(parts[:-1])
        
    return GalleryResponse(
        id=resource.get("asset_id", str(uuid.uuid4())),
        title=clean_title,
        description="A memorable moment captured in time.",
        image_url=resource.get("secure_url"),
        date="2026",
        category="corporate"
    )

@router.get("/", response_model=list[GalleryResponse])
async def get_gallery_items():
    logger.info("Fetching gallery items...")
    combined_items = []
    
    # Try fetching Cloudinary items first
    try:
        cloudinary_resources = get_resources_by_folder("samples/Gandharba_Picture")
        if cloudinary_resources:
            logger.info(f"Loaded {len(cloudinary_resources)} gallery items from Cloudinary folder 'samples/Gandharba_Picture'")
            cloudinary_items = [map_cloudinary_gallery(res, idx) for idx, res in enumerate(cloudinary_resources)]
            combined_items.extend(cloudinary_items)
    except Exception as e:
        logger.warning(f"Failed to load gallery from Cloudinary ({e}).")
        
    # Try loading from MongoDB
    db_items = []
    try:
        db = get_db()
        cursor = db.gallery.find()
        async for doc in cursor:
            db_items.append(
                GalleryResponse(
                    id=str(doc["_id"]),
                    title=doc["title"],
                    description=doc.get("description"),
                    image_url=doc["image_url"],
                    date=doc.get("date"),
                    category=doc.get("category", "corporate")
                )
            )
        if db_items:
            logger.info(f"Loaded {len(db_items)} gallery items from MongoDB.")
            combined_items.extend(db_items)
    except Exception as e:
        logger.warning(f"MongoDB connection failed for gallery router ({e}).")
        
    # If we have items from Cloudinary or DB, we can append standard defaults to make it full,
    # but filter out any duplicate IDs just in case.
    if combined_items:
        existing_ids = {item.id for item in combined_items}
        for item in DEFAULT_GALLERY:
            if item["id"] not in existing_ids:
                combined_items.append(GalleryResponse(**item))
        return combined_items
        
    # Fallback to seeded defaults if both failed
    logger.info("Returning default seeded gallery items.")
    return [GalleryResponse(**item) for item in DEFAULT_GALLERY]

@router.post("/", response_model=GalleryResponse)
async def create_gallery_item(item_in: GalleryCreate):
    try:
        db = get_db()
        item_id = str(uuid.uuid4())
        document = item_in.model_dump()
        document["_id"] = item_id
        
        await db.gallery.insert_one(document)
        logger.info(f"Created gallery item: {item_in.title}")
        return GalleryResponse(id=item_id, **item_in.model_dump())
    except Exception as e:
        logger.error(f"Failed to create gallery item in MongoDB: {e}")
        raise HTTPException(status_code=500, detail="Database write operation failed.")
