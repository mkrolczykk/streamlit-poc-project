import pandas as pd
from src.services.base_data import DataProvider

class MockDataProvider(DataProvider):
    def get_vaccine_data(self) -> pd.DataFrame:
        data = [
            {"Country": "USA", "Approach": "mRNA", "Stage": "Authorized", "Candidates": 2},
            {"Country": "USA", "Approach": "Protein Subunit", "Stage": "Phase III", "Candidates": 5},
            {"Country": "USA", "Approach": "Viral Vector", "Stage": "Phase I", "Candidates": 3},
            {"Country": "China", "Approach": "Inactivated", "Stage": "Authorized", "Candidates": 4},
            {"Country": "China", "Approach": "Protein Subunit", "Stage": "Phase II", "Candidates": 8},
            {"Country": "UK", "Approach": "Viral Vector", "Stage": "Authorized", "Candidates": 1},
            {"Country": "UK", "Approach": "mRNA", "Stage": "Phase II", "Candidates": 2},
            {"Country": "Germany", "Approach": "mRNA", "Stage": "Phase III", "Candidates": 1},
            {"Country": "Russia", "Approach": "Viral Vector", "Stage": "Authorized", "Candidates": 2},
            {"Country": "India", "Approach": "Inactivated", "Stage": "Authorized", "Candidates": 2},
            {"Country": "India", "Approach": "Protein Subunit", "Stage": "Phase III", "Candidates": 3},
            {"Country": "Australia", "Approach": "Protein Subunit", "Stage": "Phase I", "Candidates": 2},
            {"Country": "Canada", "Approach": "Plant-based", "Stage": "Phase III", "Candidates": 1},
            {"Country": "France", "Approach": "Protein Subunit", "Stage": "Phase II", "Candidates": 2},
            # Expanded dummy data
            {"Country": "USA", "Approach": "DNA", "Stage": "Pre-clinical", "Candidates": 10},
            {"Country": "China", "Approach": "mRNA", "Stage": "Pre-clinical", "Candidates": 5},
            {"Country": "UK", "Approach": "Protein Subunit", "Stage": "Pre-clinical", "Candidates": 4},
            {"Country": "Brazil", "Approach": "Inactivated", "Stage": "Phase I", "Candidates": 2},
            {"Country": "Japan", "Approach": "DNA", "Stage": "Phase I/II", "Candidates": 3},
        ]
        return pd.DataFrame(data)
