import os
from typing import Optional
from supabase import create_client, Client
from datetime import datetime
import uuid
from datetime import datetime
from dotenv import load_dotenv
from app.schemas import DiseaseInfo
from fastapi import HTTPException

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET = "scans"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

def upload_image_to_supabase(image_bytes: bytes, original_filename: str) -> str:
    ext = original_filename.split(".")[-1]
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    file_path = f"{timestamp}_{uuid.uuid4().hex}.{ext}"

    result = supabase.storage.from_(SUPABASE_BUCKET).upload(file_path, image_bytes, {"content-type": f"image/{ext}"})
    if not result or not getattr(result, "path", None):
        raise Exception("Image upload failed")
    
    public_url = f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{file_path}"
    return public_url


def get_or_save_disease_info(disease_info: DiseaseInfo) -> str:
    existing = supabase.table("diseases").select("id").eq("name", disease_info.name).execute()

    if existing.data and len(existing.data) > 0:
        return existing.data[0]["id"] 

    insert_result = supabase.table("diseases").insert({
        "name": disease_info.name,
        "category": disease_info.name.split(" - ")[0],
        "image_url": disease_info.image_url,
        "symptoms": disease_info.symptoms,
        "causes": disease_info.causes,
        "treatments": disease_info.treatments,
        "preventions": disease_info.preventions
    }).execute()

    if insert_result.data and len(insert_result.data) > 0:
        return insert_result.data[0]["id"]

    raise Exception("Failed to insert or retrieve disease ID.")

def save_scan_result(scan_data: dict, user_id: str) -> bool:
    try:
        payload = {
            "user_id": user_id,
            "image_url": scan_data.get("image_url"),
            "disease_id": scan_data.get("disease_id"),
            "disease_name": scan_data.get("name"),
            "confidence": scan_data.get("confidence"),
            "symptoms": scan_data.get("symptoms", []),
            "causes": scan_data.get("causes", []),
            "treatments": scan_data.get("treatments", []),
            "preventions": scan_data.get("preventions", [])
        }

        response = supabase.table("scans").insert(payload).execute()

        if not response or getattr(response, "data", None) is None:
            print("Insert failed or returned no data.")
            return False

        return True

    except Exception as e:
        print(f"Error saving scan result: {e}")
        raise HTTPException(status_code=400, detail="Error saving scan result: {e}")


def get_user_scan_history(user_id: str):
    response = supabase.table("scans").select("*").eq("user_id", user_id).execute()
    if not response or not response.data:
            raise HTTPException(status_code=404, detail="No scans found for user")
    return response.data

def get_scan_by_id(id: str):
    response = supabase.table("scans").select("*").eq("id", id).limit(1).execute()
    if not response or not response.data:
        raise HTTPException(status_code=404, detail=f"Scan with id {id} not found")
    
    return response.data

def delete_scan(id : str):
    response = supabase.table("scans").delete().eq("id", id).execute()
    if not response or not response.data:
        raise HTTPException(status_code=400, detail="Error deleting scan result: {response.error.message} ")
    print("Delete response:", response.data)
    return 


def add_scan_feedback(scan_id: str, helpful: bool, comments: Optional[str] = None):
    feedback_payload = {
        "feedback": {
            "helpful": helpful,
            "comments": comments,
            "timestamp": int(datetime.utcnow().timestamp())
        }
    }

    response = supabase.table("scans").update(feedback_payload).eq("id", scan_id).execute()

    if not response:
        raise HTTPException(status_code=400, detail=f"Failed to add feedback: {response.error.message}")
    
    return True



def get_all_diseases():
    response = supabase.table("diseases").select("*").order("name", desc=False).execute()
    return response.data

def get_disease_by_id(disease_id: str):
    response = supabase.table("diseases").select("*").eq("id", disease_id).limit(1).execute()
    return response.data[0] if response.data else None

def search_diseases(search: str):
    response = supabase.table("diseases").select("*").ilike("name", f"%{search}%").execute()
    return response.data

def get_diseases_by_category(category: str):
    response = supabase.table("diseases").select("*").ilike("category", f"%{category}%").execute()
    return response.data
