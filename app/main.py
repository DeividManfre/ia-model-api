from fastapi import fastapi
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

from app.routes import auth, inference
from app.utils.logger import setup_logging
from app.utils.rate_limiter import limiter


app = FastAPI(title="IA Model Serving API", version="0.1-Alpha")
setup_logging(app)
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Try again later."},
    )

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(inference.router, prefix="/inference", tags=["Inference"])

@app.get("/")
async def root():
    return {"message": "Welcome to the IA Model Serving API!"}