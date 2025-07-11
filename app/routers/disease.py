from fastapi import APIRouter, HTTPException, Query
from app.utils.utils import validate_uuid
from typing import List
from app.schemas import Disease
from app.core.supabase import (
    get_all_diseases,
    get_disease_by_id,
    search_diseases,
    get_diseases_by_category
)

router = APIRouter()

@router.get("/")
def fetch_all_diseases():
    return get_all_diseases()

@router.get("/search", response_model=List[Disease])
def fetch_searched_diseases(search: str = Query(..., description="Search query for disease name")):
    result = search_diseases(search)
    if not result:
        raise HTTPException(status_code=404, detail="No matching diseases found")
    return result

@router.get("/category", response_model=List[Disease])
def fetch_diseases_by_category(category: str = Query(..., description="Disease category name")):
    result = get_diseases_by_category(category)
    if not result:
        raise HTTPException(status_code=404, detail="No diseases found in this category")
    return result

@router.get("/{disease_id}", response_model=Disease)
def fetch_disease_by_id(disease_id: str):
    validate_uuid(disease_id)
    result = get_disease_by_id(disease_id)
    if not result:
        raise HTTPException(status_code=404, detail="Disease not found")
    return result

