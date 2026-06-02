from fastapi import APIRouter, HTTPException
from app.models.contact import ContactCreate, ContactResponse
from app.database import get_db
from datetime import datetime, timezone
import uuid
import logging

logger = logging.getLogger("uvicorn")
router = APIRouter(prefix="/api/contact", tags=["Contact"])

@router.post("/", response_model=ContactResponse)
async def create_contact(contact_in: ContactCreate):
    contact_id = str(uuid.uuid4())
    created_at = datetime.now(timezone.utc)
    
    document = contact_in.model_dump()
    document["_id"] = contact_id
    document["created_at"] = created_at
    
    try:
        db = get_db()
        await db.contacts.insert_one(document)
        logger.info("Successfully saved contact message to MongoDB.")
    except Exception as e:
        logger.error(f"MongoDB connection/write failed for contact submission: {e}")
        raise HTTPException(
            status_code=503,
            detail="Contact submission failed because database is unavailable. Please try again shortly."
        )
    
    return ContactResponse(
        id=contact_id,
        name=contact_in.name,
        email=contact_in.email,
        subject=contact_in.subject,
        message=contact_in.message,
        created_at=created_at
    )

@router.get("/", response_model=list[ContactResponse])
async def get_contacts():
    """Retrieve all contacts (for debugging/admin purposes)"""
    contacts_list = []
    
    try:
        db = get_db()
        cursor = db.contacts.find()
        async for doc in cursor:
            contacts_list.append(
                ContactResponse(
                    id=doc["_id"],
                    name=doc["name"],
                    email=doc["email"],
                    subject=doc["subject"],
                    message=doc["message"],
                    created_at=doc["created_at"]
                )
            )
        logger.info(f"Fetched {len(contacts_list)} contacts from MongoDB.")
        return contacts_list
    except Exception as e:
        logger.error(f"Failed to fetch contacts from MongoDB: {e}")
        raise HTTPException(
            status_code=503,
            detail="Unable to fetch contacts because database is unavailable."
        )
