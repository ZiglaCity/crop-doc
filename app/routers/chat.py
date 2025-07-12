from fastapi import APIRouter, HTTPException
from app.schemas import ChatRequest, ChatResponse
from app.core.get_ai_chat_response import get_gemini_response

router = APIRouter()

@router.get('/')
def get():
    return "Starting chat..."

@router.post("/message", response_model=ChatResponse)
async def chat_with_ai(payload: ChatRequest):
    try:
        response, suggestions = get_gemini_response(payload.messages, payload.language, payload.context)
        return {"reply": response, "suggestedQuestions": suggestions}
    except Exception as e:
        print("Gemini error:", e)
        raise HTTPException(status_code=500, detail="Error getting response from AI")
