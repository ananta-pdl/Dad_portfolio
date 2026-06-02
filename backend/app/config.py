from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    mongodb_uri: str = "mongodb://localhost:27017"
    database_name: str = "baba_portfolio"

    # Cloudinary Config
    cloudinary_cloud_name: str = "dummy_cloud_name"
    cloudinary_api_key: str = "dummy_api_key"
    cloudinary_api_secret: str = "dummy_api_secret"

    # Cloudinary folder paths
    cloudinary_music_folder: str = "samples/Gandharba_Music"
    cloudinary_pictures_folder: str = "samples/Gandharba_picture"

    # CORS configuration (set frontend domains here)
    cors_origins: str = "https://dad-portfolio.vercel.app"

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()

