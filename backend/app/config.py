from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    mongodb_uri: str = "mongodb://127.0.0.1:27017"
    database_name: str = "baba_portfolio"

    # Cloudinary Config
    cloudinary_cloud_name: str = "your_cloud_name"
    cloudinary_api_key: str = "your_api_key"
    cloudinary_api_secret: str = "your_api_secret"

    # Cloudinary folder paths
    cloudinary_music_folder: str = "samples/Gandharba_Music"
    cloudinary_pictures_folder: str = "samples/Gandharba_picture"

    # CORS configuration (comma-separated frontend origins)
    cors_origins: str = "http://localhost:5173"

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()

