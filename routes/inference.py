from fastapi import APIRouter, UploadFile, HTTPException
from app.server.jwt_handler import JWTHandler, Depends
from app.server.celery_tasks import process_inference
