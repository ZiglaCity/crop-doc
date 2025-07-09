from typing import List
from pydantic import BaseModel

class PredictionResponse(BaseModel):
    label: str
    confidence: float

class ScanResponse(BaseModel):
    diseaseId: str
    name: str
    image_url : str
    symptoms: List[str]
    causes: List[str]
    treatments: List[str]
    preventions: List[str]
    confidence: float


class DiseaseInfo(BaseModel):
    name : str
    image_url : str
    symptoms : List[str]
    causes: List[str]
    treatments: List[str]
    preventions: List[str]


