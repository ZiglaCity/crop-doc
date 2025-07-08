from typing import List
from pydantic import BaseModel

class PredictionResponse(BaseModel):
    label: str
    confidence: float

class ScanResponse(BaseModel):
    diseaseId: str
    name: str
    confidence: float
    symptoms: List[str]
    causes: List[str]
    treaments: List[str]
    preventions: List[str]
    