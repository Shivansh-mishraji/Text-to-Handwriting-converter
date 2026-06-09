import os
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

def main():
    print("Generating synthetic dataset...")
    
    # Create a synthetic dataset for text vibes
    data = [
        # Formal
        ("To whom it may concern, I am writing to formally request a leave of absence.", "Formal"),
        ("Please find attached the signed contract for your review and processing.", "Formal"),
        ("We regret to inform you that your application has not been successful at this time.", "Formal"),
        ("The board of directors cordially invites you to the annual general meeting.", "Formal"),
        ("This document outlines the standard operating procedures for the department.", "Formal"),
        ("Dear Sir/Madam, I would like to inquire about the status of my order.", "Formal"),
        
        # Creative
        ("The sunset painted the sky in brilliant hues of orange, pink, and violet.", "Creative"),
        ("Once upon a time, in a kingdom hidden beneath the waves, lived a curious mermaid.", "Creative"),
        ("Her words danced on the page like leaves caught in a gentle autumn breeze.", "Creative"),
        ("I wandered lonely as a cloud that floats on high o'er vales and hills.", "Creative"),
        ("Music is the universal language of mankind, echoing through the corridors of time.", "Creative"),
        
        # Urgent
        ("Warning: Evacuate the building immediately! Fire alarm activated in sector 7.", "Urgent"),
        ("Please reply ASAP. The deadline is in 10 minutes and we need your approval.", "Urgent"),
        ("EMERGENCY! We are out of coffee in the breakroom. This is not a drill.", "Urgent"),
        ("Alert! Your server is down and losing traffic rapidly. Fix it now!", "Urgent"),
        ("Hurry up! The train is leaving in exactly two minutes. Run!", "Urgent"),
        
        # Casual
        ("Hey man, what's up? Are we still hanging out tonight?", "Casual"),
        ("Just grabbed some pizza. It's so good! You should come over.", "Casual"),
        ("lol that meme you sent me was hilarious 😂", "Casual"),
        ("I'm so tired today. Just gonna chill and watch Netflix all evening.", "Casual"),
        ("Yeah sure, sounds good to me. See ya later!", "Casual"),
        ("Can you pick up some milk on your way home? Thanks!", "Casual"),
    ]
    
    df = pd.DataFrame(data, columns=["text", "vibe"])
    
    print("Training TF-IDF Vectorizer...")
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(df['text'])
    y = df['vibe']
    
    print("Training Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X, y)
    
    # Save artifacts
    os.makedirs("ml", exist_ok=True)
    
    print("Exporting artifacts...")
    joblib.dump(vectorizer, "ml/vectorizer.pkl")
    joblib.dump(model, "ml/vibe_model.pkl")
    
    print("Done! Model trained and saved to ml/vibe_model.pkl")

if __name__ == "__main__":
    main()
