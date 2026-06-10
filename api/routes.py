import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from ml.inference import engine
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class TextPayload(BaseModel):
    text: str = Field(..., description="Text to analyze and style")

class StylingRecommendation(BaseModel):
    vibe: str
    font: str
    color: str
    flow: int
    size: int

@router.post("/analyze-text", response_model=StylingRecommendation)
async def analyze_text(payload: TextPayload):
    try:
        vibe = engine.predict(payload.text)
        
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
    except Exception as e:
        logger.error(f"Error in analyze_text: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during analysis")
