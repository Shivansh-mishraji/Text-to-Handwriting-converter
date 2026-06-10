import os
import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
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

# Serve Frontend Static Files
os.makedirs("frontend", exist_ok=True)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def read_root():
    index_path = os.path.join("frontend", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Frontend not found"}

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting HandWrite Pro Server on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
