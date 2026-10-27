import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    APP_NAME: str = "Thari"
    APP_TITLE: str = "Thari - Handloom Weavers D2C Platform"
    APP_DESCRIPTION: str = "Direct-to-Consumer platform connecting heritage Indian handloom weavers with conscious consumers."
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Server configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Paths
    BASE_DIR: Path = BASE_DIR
    DATA_DIR: Path = BASE_DIR / "data"
    STATIC_DIR: Path = BASE_DIR / "static"
    TEMPLATES_DIR: Path = BASE_DIR / "templates"
    
    # Platform Fair Share Defaults (Min 75% goes directly to artisan)
    MIN_ARTISAN_SHARE_PERCENT: float = 75.0
    DEFAULT_ARTISAN_SHARE_PERCENT: float = 82.0
    PLATFORM_FEE_PERCENT: float = 5.0
    
    # Security & API
    API_V1_PREFIX: str = "/api/v1"
    CORS_ORIGINS: list[str] = ["*"]
    ENABLE_SIMULATED_ESCROW: bool = True
    ENABLE_SAMPLE_DATA_SEEDING: bool = True

settings = Settings()
