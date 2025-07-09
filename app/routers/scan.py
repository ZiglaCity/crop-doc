from fastapi import APIRouter, File, UploadFile
from app.schemas import DiseaseInfo, ScanResponse
from app.model import load_model, predict_image
from app.utils import read_imagefile
from app.core.supabase import upload_image_to_supabase, save_disease_info
from app.core.request_disease_info import get_more_info

router = APIRouter()

model, class_labels = load_model()

@router.get('/')
def scan():
    return "Scanning endpoint setup..."

@router.post("/", response_model=ScanResponse)
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = read_imagefile(image_bytes)
    predicted_label, confidence = predict_image(image, model, class_labels)
    image_url = upload_image_to_supabase(image_bytes= image_bytes, original_filename = file.filename)
    
    result = get_more_info(predicted_label)
    result["image_url"] = image_url

    disease_info = DiseaseInfo(**result)
    disease_id = save_disease_info(disease_info)
    print(result)

    result["confidence"] = confidence
    result["diseaseId"] = disease_id

    return result

