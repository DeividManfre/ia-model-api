from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.services.jwt_handler import verify_token
from app.services.celery_tasks import process_inference
from app.utils.rate_limiter import limiter

router = APIRouter()

class InferenceRequest(BaseModel):
    text: str

@router.post("/run")
@limiter.limit("5/minute")
async def run_inference(request: InferenceRequest, user=Depends(verify_token)):
    if not request.text.strip():
        raise HTTPException(400, "The 'text' field cannot be empty")

    task = process_inference.delay(request.text)
    return {"task_id": task.id, "status": "processing"}