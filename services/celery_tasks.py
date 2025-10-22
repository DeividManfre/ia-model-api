from celery import Celery
import subprocess
import os
import tempfile
import uuid
import json

celery = Celery(__name__, broker="redis://redis:6379/0")

MODEL_NAME = os.getenv("MODEL_NAME", "llava:7b")  # modelo de IA (ex: Qwen2-VL, Gemma, LLaVA etc.)

@celery.task
def process_inference(file_name: str, file_bytes: bytes = None):
    try:
        tmp_path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}_{file_name}")
        with open(tmp_path, "wb") as f:
            f.write(file_bytes)

        cmd = [
            "ollama", "run", MODEL_NAME,
            "--prompt", f"Descreva brevemente esta imagem: {tmp_path}"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        output = result.stdout.strip()
        return json.dumps({"status": "success", "output": output})

    except subprocess.CalledProcessError as e:
        return json.dumps({"status": "error", "stderr": e.stderr})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})
