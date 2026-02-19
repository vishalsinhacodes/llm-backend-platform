from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse


from app.models.schemas import ChatRequest, ChatResponse
from app.services.groq_client import chat_completion, stream_chat


router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        reply = chat_completion(req.message)
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/stream")
def chat_stream(req: ChatRequest):
    def generator():
        for token in stream_chat(req.message):
            yield token
            
    return StreamingResponse(generator(), media_type="text/plain")