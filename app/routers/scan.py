from fastapi import APIRouter, File, UploadFile
from app.schemas import PredictionResponse, ScanResponse
from app.model import load_model, predict_image
from app.utils import read_imagefile
from app.core.supabase import upload_image_to_supabase

router = APIRouter()

model, class_labels = load_model()

@router.get('/')
def scan():
    return "Scanning endpoint setup..."

@router.post("/")
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = read_imagefile(image_bytes)
    predicted_label, confidence = predict_image(image, model, class_labels)
    image_url = upload_image_to_supabase(image_bytes= image_bytes, original_filename = file.filename)

    # send the perdicted label to an llm to give more detials, possible causes, symptoms, confidence, etc...

    return {"label": predicted_label, "confidence": confidence, "image_url": image_url}

