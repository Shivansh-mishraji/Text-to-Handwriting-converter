from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import joblib
import os

app = FastAPI()

# ML Model Loading
MODEL_PATH = "ml/vibe_model.pkl"
VECTORIZER_PATH = "ml/vectorizer.pkl"
vibe_model = None
vectorizer = None

def load_ml_assets():
    global vibe_model, vectorizer
    if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
        vibe_model = joblib.load(MODEL_PATH)
        vectorizer = joblib.load(VECTORIZER_PATH)
        print("ML Models loaded successfully!")
    else:
        print("ML Models not found. Run train_model.py first.")

load_ml_assets()

class TextPayload(BaseModel):
    text: str

@app.post("/api/analyze-text")
def analyze_text(payload: TextPayload):
    if not vibe_model or not vectorizer:
        raise HTTPException(status_code=503, detail="ML Model not available")
    
    if not payload.text.strip():
        # Default fallback
        return {"vibe": "Casual", "font": "Pacifico", "color": "#0a3d91", "flow": 7, "size": 32}

    # Transform text
    X = vectorizer.transform([payload.text])
    vibe = vibe_model.predict(X)[0]
    
    # Map vibe to styling recommendations
    recommendation = {
        "vibe": vibe,
        "font": "Satisfy",
        "color": "#0a3d91",
        "flow": 7,
        "size": 32
    }
    
    if vibe == "Formal":
        recommendation.update({"font": "Great Vibes", "color": "#1a1a1a", "flow": 5, "size": 24})
    elif vibe == "Creative":
        recommendation.update({"font": "Dancing Script", "color": "#0a3d91", "flow": 9, "size": 40})
    elif vibe == "Urgent":
        recommendation.update({"font": "Caveat", "color": "#1a1a1a", "flow": 8, "size": 48})
    elif vibe == "Casual":
        recommendation.update({"font": "Satisfy", "color": "#0a3d91", "flow": 7, "size": 32})
        
    return recommendation

# Serve Frontend
os.makedirs("frontend", exist_ok=True)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def read_root():
    return FileResponse("frontend/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
