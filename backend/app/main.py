from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config import settings
from app.database import db_manager
from app.routers import contact, music, gallery
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    logger.info("Starting up FastAPI Portfolio Backend...")
    try:
        db_manager.connect()
    except Exception as e:
        logger.warning(f"Startup MongoDB connection attempt failed: {e}. App will run with in-memory fallbacks.")
    
    yield
    
    # Shutdown actions
    logger.info("Shutting down FastAPI Portfolio Backend...")
    db_manager.disconnect()

app = FastAPI(
    title="Corporate & Musician Portfolio API",
    description="API for managing contact information, achievements gallery, and musical recordings.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(contact.router)
app.include_router(music.router)
app.include_router(gallery.router)

@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "Welcome to the Corporate & Musician Portfolio API. Access /docs for API documentation.",
        "config": {
            "database_name": settings.database_name,
            "cors_origins_configured": settings.cors_origins_list
        }
    }
