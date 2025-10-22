from celery import Celery
import subprocess
import os
import json
import uuid
import tempfile
from datetime import datetime
from app.services.s3_service import upload_file_to_s3

celery = Celery(__name__, broker="redis://redis:6379/0")
MODEL_NAME = os.getenv("MODEL_NAME", "llava:7b")  # modelo LLM 
S3_BUCKET = os.getenv("S3_BUCKET", "ai-model-results")

@celery.task
def process_inference(prompt_text: str):
    try:
        prompt = f"Analyze the following text and generate a structured response:\n\n{prompt_text}"

        cmd = ["ollama", "run", MODEL_NAME, "--prompt", prompt]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        output = result.stdout.strip()

        result_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        result_data = {
            "id": result_id,
            "model": MODEL_NAME,
            "prompt": prompt_text,
            "response": output,
            "timestamp": timestamp,
        }

        tmp_path = os.path.join(tempfile.gettempdir(), f"{result_id}.json")
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)

        s3_key = f"results/{result_id}.json"
        s3_url = upload_file_to_s3(tmp_path, S3_BUCKET, s3_key)

        return {"status": "success", "s3_url": s3_url, "model": MODEL_NAME}

    except subprocess.CalledProcessError as e:
        return {"status": "error", "stderr": e.stderr}
    except Exception as e:
        return {"status": "error", "message": str(e)}