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

def _folder_candidates(folder_path: str) -> list[str]:
    """Generate likely folder path variants (case and optional prefix)."""
    raw = (folder_path or "").strip().strip("/")
    if not raw:
        return []

    parts = raw.split("/")
    candidates = {
        raw,
        raw.lower(),
        raw.upper(),
        "/".join(p.capitalize() for p in parts),
    }

    if not raw.lower().startswith("samples/"):
        candidates.add(f"samples/{raw}")
        candidates.add(f"samples/{raw.lower()}")
        candidates.add(f"samples/{'/'.join(p.capitalize() for p in parts)}")
        if "/samples/" in raw.lower():
            idx = raw.lower().find("/samples/")
            normalized = raw[idx + 1:]  # drop leading prefix before "samples/"
            candidates.add(normalized)
            candidates.add(normalized.lower())

    return [c for c in candidates if c]

def get_resources_by_folder_robust(folder_path: str):
    """
    Try multiple folder variants and return first non-empty result.
    This prevents breakage from minor folder casing/prefix mismatches.
    """
    for candidate in _folder_candidates(folder_path):
        resources = get_resources_by_folder(candidate)
        if resources:
            logger.info(f"Cloudinary folder resolved to '{candidate}'")
            return resources
    logger.warning(f"No Cloudinary resources found for folder variants of '{folder_path}'")
    return []
