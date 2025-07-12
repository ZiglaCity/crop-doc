from fastapi import FastAPI, File, UploadFile
from app.model import load_model, predict_image
from app.schemas import PredictionResponse
from app.utils.utils import read_imagefile
from app.routers import scan, disease, chat

app = FastAPI()

model, class_labels = load_model()

API_URL = 'https://github.com/steveAzo/ccmt-api/releases/download/v1.0/best_model_v1_71percent.pth'

@app.post("/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...)):
    image = read_imagefile(await file.read())
    predicted_label, confidence = predict_image(image, model, class_labels)
    return {"label": predicted_label, "confidence": confidence}

app.include_router(scan.router, prefix="/scan", tags=["Scan"])

app.include_router(disease.router, prefix="/diseases", tags=["Diseases"])

app.include_router(chat.router, prefix="/chat", tags=["Chat"])