import os

class Config:
    PAGE_TITLE = "COVID-19 Vaccine Dashboard"
    PAGE_ICON = "💉"
    LAYOUT = "wide"
    
    # Data Source: MOCK, POSTGRES
    DATA_SOURCE = os.getenv("DATA_SOURCE", "MOCK").upper()
    
    # Postgres Configuration
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "vaccines")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
    
    @property
    def UPDATE_INTERVAL_SECONDS(self):
        return 3600 # 1 hour default
