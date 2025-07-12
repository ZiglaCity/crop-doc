from typing import Optional, List, Dict
from pydantic import BaseModel
from datetime import datetime

class PredictionResponse(BaseModel):
    label: str
    confidence: float

# later change the disease id to just the scan rsult id
class ScanResponse(BaseModel):
    disease_id: str
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


class Location(BaseModel):
    latitude: float
    longitude: float
    name: Optional[str] = None

class FeedbackStructure(BaseModel):
    helpful: bool
    comments: Optional[str] = None
    timestamp: Optional[datetime] = None 

class Feedback(BaseModel):
    scan_id: str
    helpful: bool
    comments: Optional[str] = None

class ScanInfo(BaseModel):
    id: str
    user_id: str
    image_url: str
    thumbnail_url: Optional[str] = None
    disease_id: str
    disease_name: str
    confidence: float
    symptoms: List[str]
    causes: List[str]
    treatments: List[str]
    preventions: List[str]
    timestamp: Optional[str] = None  # Use datetime on FastAPI endpoint if needed
    location: Optional[Location] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None
    feedback: Optional[FeedbackStructure] = None 


class Disease(BaseModel):
    id: str
    name: str
    category: str
    image_url: Optional[str]
    symptoms: List[str]
    causes: List[str]
    treatments: List[str]
    preventions: List[str]
    created_at: Optional[str]

    class Config:
        orm_mode = True
    

class ContextData(BaseModel):
    recentScans: Optional[List[str]]
    location: Optional[str]
    weather: Optional[str]

class MessageCreate(BaseModel):
    user_id: str
    session_id: str
    role: str  # "user", "assistant", "system"
    content: str
    related_scan_id: Optional[str] = None
    audio_uri: Optional[str] = None
    context_data: Optional[ContextData]

class MessageResponse(BaseModel):
    id: str
    user_id: str
    session_id: str
    role: str
    content: str
    timestamp: str
    related_scan_id: Optional[str]
    audio_uri: Optional[str]
    context_data: Optional[Dict]


class ChatMessage(BaseModel):
    role: str  # "user" | "assistant" | "system"
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    language: Optional[str] = "en"
    context: Optional[dict] = None  # Can include scan result or location

class ChatResponse(BaseModel):
    reply: str
    suggestedQuestions: List[str]
