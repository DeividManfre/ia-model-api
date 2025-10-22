from fastapi import APIRouter, Depends, UploadFile, HTTPException
from app.services.jwt_handler import verify_token
from app.services.celery_tasks import process_inference
from app.utils.rate_limiter import limiter

router = APIRouter()

@router.post("/run")
@limiter.limit("5/minute")
async def run_inference(file: UploadFile, user=Depends(verify_token)):
    if not file.filename.endswith((".png", ".jpg", ".jpeg")):
        raise HTTPException(400, "Invalid file type")
    
    file_bytes = await file.read()
    task = process_inference.delay(file.filename, file_bytes)
    return {"task_id": task.id, "status": "processing"}
