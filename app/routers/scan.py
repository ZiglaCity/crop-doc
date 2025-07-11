from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from app.schemas import DiseaseInfo, ScanResponse, ScanInfo, Feedback
from typing import List
from app.model import load_model, predict_image
from app.utils.utils import read_imagefile
from app.utils.get_current_user import get_current_user
from app.core.supabase import upload_image_to_supabase, get_or_save_disease_info, get_user_scan_history, get_scan_by_id, delete_scan, save_scan_result, add_scan_feedback
from app.core.request_disease_info import get_more_info

router = APIRouter()

model, class_labels = load_model()

@router.get('/')
def scan():
    return "Scanning endpoint setup..."

@router.post("/", response_model=ScanResponse)
async def predict(
        file: UploadFile = File(..., description="The image of the crop to be scanned"),
        user_id: str = Depends(get_current_user)
    ):
    try:
        image_bytes = await file.read()
        image = read_imagefile(image_bytes)

        predicted_label, confidence = predict_image(image, model, class_labels)

        image_url = upload_image_to_supabase(image_bytes= image_bytes, original_filename = file.filename)
        
        # before getting more info, check if disease already exist in database...
        result = get_more_info(predicted_label)
        result["image_url"] = image_url

        disease_info = DiseaseInfo(**result)
        disease_id = get_or_save_disease_info(disease_info)

        result["confidence"] = confidence
        result["disease_id"] = disease_id #later return the scan id instead

        success = save_scan_result(scan_data=result, user_id=user_id)
        if not success:
            raise HTTPException("Error saving scan result")
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scan prediction failed: {e}")


@router.get('/history', response_model=List[ScanInfo])
def get_scan_history(user_id: str = Depends(get_current_user)):
    result = get_user_scan_history(user_id)
    if not result:
        raise HTTPException(status_code=404, detail="No scans found for user")
    return result

@router.post('/feedback')
def add_feedback_to_scan(feedback: Feedback):
    success = add_scan_feedback(
        scan_id=feedback.scan_id,
        helpful=feedback.helpful,
        comments=feedback.comments
    )
    return {"message": "Feedback submitted successfully", "success": success}


@router.get('/history/{id}', response_model=ScanInfo)
def get_scan_details(id: str, user_id: str = Depends(get_current_user)):
    result = get_scan_by_id(id)

    if not result:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    scan = result[0]
    if scan["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized access to scan")

    return scan


@router.delete('/history/{id}')
def delete_scan_result(id: str, user_id: str = Depends(get_current_user)):
    result = get_scan_by_id(id)

    if not result:
        raise HTTPException(status_code=404, detail="Scan not found")

    scan = result[0]
    if scan["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized to delete this scan")

    delete_scan(id)
    return {"message": "Scan deleted successfully"}
