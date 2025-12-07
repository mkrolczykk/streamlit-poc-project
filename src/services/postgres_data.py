import pandas as pd
from sqlalchemy import create_engine
from src.services.base_data import DataProvider
from src.config import Config

class PostgresDataProvider(DataProvider):
    def __init__(self):
        # Create connection string
        self.db_url = f"postgresql://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}"
        self.engine = create_engine(self.db_url)

    def get_vaccine_data(self) -> pd.DataFrame:
        """
        Fetches data from the database. 
        Assumes a table 'vaccine_candidates' exists with columns:
        country, approach, stage, candidate_count
        """
        query = """
            SELECT
                country AS "Country",
                approach AS "Approach",
                stage AS "Stage",
                candidate_count AS "Candidates"
            FROM
                vaccine_candidates
        """
        try:
            return pd.read_sql(query, self.engine)
        except Exception as e:
            # Fallback or error handling for production
            # For now, we allow it to crash so the issue is visible, or return empty
            raise RuntimeError(f"Failed to fetch data from Postgres: {e}")
