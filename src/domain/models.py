from dataclasses import dataclass

@dataclass
class VaccineCandidate:
    country: str
    approach: str
    stage: str
    candidate_count: int
