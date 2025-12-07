"""
Configuration settings for the COVID-19 Vaccine Dashboard.
Supports environment variable overrides for production deployment.
"""
import os
from typing import Literal

DataSourceType = Literal["MOCK", "POSTGRES"]


class Config:
    """Application configuration with environment variable support."""
    
    # Page Settings
    PAGE_TITLE: str = "COVID-19 Vaccine Dashboard"
    PAGE_ICON: str = "💉"
    LAYOUT: str = "wide"
    
    # Data Source: MOCK or POSTGRES
    DATA_SOURCE: DataSourceType = os.getenv("DATA_SOURCE", "MOCK").upper()  # type: ignore
    
    # PostgreSQL Configuration
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_NAME: str = os.getenv("DB_NAME", "vaccines")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "postgres")
    
    # Cache Settings
    UPDATE_INTERVAL_SECONDS: int = 3600  # 1 hour
    
    @classmethod
    def get_database_url(cls) -> str:
        """Get the PostgreSQL connection URL."""
        return f"postgresql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"
