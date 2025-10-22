from celery import celery as cl
import time 

celery = cl.Celery(__name__, broker="redis://localhost:6379/0")

@celery.task
def process_inference(file_name: str):
    time.sleep(5) # Simulate a time-consuming inference process ;)
    return f"Inference processed for file: {file_name}"