import os
import logging
from fastapi import FastAPI
from fastapi.responses import FileResponse
from api.routes import router as api_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="HandWrite Pro API",
    description="ML-Powered Handwriting Generator Backend",
    version="2.0.0"
)

# Include Modularized API Routes
app.include_router(api_router, prefix="/api", tags=["Analysis"])

@app.get("/")
def read_root():
    return FileResponse("index.html")

@app.get("/style.css")
def get_style():
    return FileResponse("style.css")

@app.get("/app.js")
def get_app():
    return FileResponse("app.js")

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting HandWrite Pro Server on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
