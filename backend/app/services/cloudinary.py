import logging
import cloudinary
import cloudinary.api
from cloudinary.search import Search
from app.config import settings

logger = logging.getLogger("uvicorn")

# Initialize Cloudinary config once
cloudinary.config(
    cloud_name=settings.cloudinary_cloud_name,
    api_key=settings.cloudinary_api_key,
    api_secret=settings.cloudinary_api_secret,
    secure=True
)

def get_resources_by_folder(folder_path: str):
    """
    Fetch all resources belonging to a specific visual folder in the Media Library.
    Uses the Cloudinary Search API which is accurate for folder-level queries.
    """
    try:
        logger.info(f"Querying Cloudinary Search API for folder: {folder_path}")
        results = Search().expression(f'folder:"{folder_path}"').with_field('context').with_field('tags').max_results(100).execute()
        resources = results.get("resources", [])
        logger.info(f"Successfully retrieved {len(resources)} assets from folder '{folder_path}'")
        return resources
    except Exception as e:
        logger.error(f"Error querying Cloudinary Search API for folder '{folder_path}': {e}")
        return []
