from typing import Protocol, List
import pandas as pd
from src.domain.models import VaccineCandidate

class DataProvider(Protocol):
    def get_vaccine_data(self) -> pd.DataFrame:
        """Returns the vaccine data as a pandas DataFrame."""
        ...
