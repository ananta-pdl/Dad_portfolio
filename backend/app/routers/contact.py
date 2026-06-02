from fastapi import APIRouter, HTTPException
from app.models.contact import ContactCreate, ContactResponse
from app.database import get_db
from datetime import datetime, timezone
import uuid
import logging

logger = logging.getLogger("uvicorn")
router = APIRouter(prefix="/api/contact", tags=["Contact"])

# In-memory fallback database
in_memory_contacts = []

@router.post("/", response_model=ContactResponse)
async def create_contact(contact_in: ContactCreate):
    contact_id = str(uuid.uuid4())
    created_at = datetime.now(timezone.utc)
    
    document = contact_in.model_dump()
    document["_id"] = contact_id
    document["created_at"] = created_at
    
    try:
        db = get_db()
        # Attempt to insert with a short timeout to prevent long hangs if MongoDB is unreachable
        # motor allows setting serverSelectionTimeoutMS on the client, but here we can just try to run it
        await db.contacts.insert_one(document)
        logger.info("Successfully saved contact message to MongoDB.")
    except Exception as e:
        logger.warning(f"MongoDB connection/write failed ({e}). Falling back to in-memory storage.")
        in_memory_contacts.append(document)
        logger.info(f"Saved message in-memory (Total messages: {len(in_memory_contacts)})")
    
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
    
    # Try reading from MongoDB
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
        logger.warning(f"Failed to fetch contacts from MongoDB: {e}. Returning in-memory list.")
        
    # Return in-memory list if DB fails
    for doc in in_memory_contacts:
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
    return contacts_list
