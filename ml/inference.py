import os
import joblib
import logging

logger = logging.getLogger(__name__)

class VibeInferenceEngine:
    def __init__(self, model_path="ml/pipeline.pkl"):
        self.model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), model_path)
        self.pipeline = None

    def load_model(self):
        if os.path.exists(self.model_path):
            try:
                self.pipeline = joblib.load(self.model_path)
                logger.info(f"Loaded ML model from {self.model_path}")
                return True
            except Exception as e:
                logger.error(f"Failed to load ML model: {e}")
        else:
            logger.warning(f"Model path {self.model_path} does not exist.")
        return False

    def predict(self, text: str) -> str:
        if not text.strip():
            return "Casual" # Default fallback
            
        if self.pipeline is None:
            if not self.load_model():
                return "Casual"
                
        try:
            prediction = self.pipeline.predict([text])[0]
            return prediction
        except Exception as e:
            logger.error(f"Inference error: {e}")
            return "Casual"

engine = VibeInferenceEngine()
engine.load_model()
