import os
from supabase import create_client, Client
import uuid
from datetime import datetime
from dotenv import load_dotenv
from app.schemas import DiseaseInfo

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
    # if res.error:
    #     raise Exception("Image upload failed")

    public_url = f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{file_path}"
    return public_url


def save_disease_info(disease_info: DiseaseInfo) -> str:
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