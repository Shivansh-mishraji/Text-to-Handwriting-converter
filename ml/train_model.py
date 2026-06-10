import os
import json
import joblib
import pandas as pd
from datetime import datetime
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import accuracy_score, classification_report

def get_dataset():
    data = [
        # Formal
        ("To whom it may concern, I am writing to formally request a leave of absence.", "Formal"),
        ("Please find attached the signed contract for your review and processing.", "Formal"),
        ("We regret to inform you that your application has not been successful at this time.", "Formal"),
        ("The board of directors cordially invites you to the annual general meeting.", "Formal"),
        ("This document outlines the standard operating procedures for the department.", "Formal"),
        ("Dear Sir/Madam, I would like to inquire about the status of my order.", "Formal"),
        ("I am writing to express my interest in the recently advertised position.", "Formal"),
        ("We acknowledge receipt of your correspondence dated the 5th of May.", "Formal"),
        ("Enclosed please find the invoice for the services rendered last month.", "Formal"),
        ("I respectfully request an extension for the submission of the project report.", "Formal"),
        ("Your prompt attention to this matter would be highly appreciated.", "Formal"),
        ("We are pleased to announce the successful completion of the merger.", "Formal"),
        ("Please be advised that the policy terms have been updated effective immediately.", "Formal"),
        ("I am writing to formally tender my resignation from the position of Manager.", "Formal"),
        ("The committee has reviewed your proposal and approved the requested budget.", "Formal"),
        ("We apologize for any inconvenience this may have caused.", "Formal"),
        ("Please do not hesitate to contact us should you require further assistance.", "Formal"),
        ("The terms and conditions of the agreement are binding and non-negotiable.", "Formal"),
        ("I would be grateful if you could confirm your attendance at the upcoming seminar.", "Formal"),
        ("This letter serves as formal notification of the termination of your lease.", "Formal"),
        
        # Creative
        ("The sunset painted the sky in brilliant hues of orange, pink, and violet.", "Creative"),
        ("Once upon a time, in a kingdom hidden beneath the waves, lived a curious mermaid.", "Creative"),
        ("Her words danced on the page like leaves caught in a gentle autumn breeze.", "Creative"),
        ("I wandered lonely as a cloud that floats on high o'er vales and hills.", "Creative"),
        ("Music is the universal language of mankind, echoing through the corridors of time.", "Creative"),
        ("The moon was a ghostly galleon tossed upon cloudy seas.", "Creative"),
        ("Shadows lengthened as the ancient forest awoke to the symphony of the night.", "Creative"),
        ("He wove a tapestry of dreams from the fragile threads of memory.", "Creative"),
        ("The stars blinked like diamonds scattered across a velvet canvas.", "Creative"),
        ("A gentle whisper of the wind carried the secrets of forgotten lovers.", "Creative"),
        ("Time slipped through his fingers like grains of golden sand.", "Creative"),
        ("The old book smelled of dust, magic, and countless untold adventures.", "Creative"),
        ("Raindrops raced down the window pane, a melancholic ballet of nature.", "Creative"),
        ("Her laughter was a melody that brought color to a grayscale world.", "Creative"),
        ("The dragon's breath was a fiery dawn breaking the eternal winter.", "Creative"),
        ("They sailed across the sea of imagination on a ship made of starlight.", "Creative"),
        ("The city pulsed with a restless energy, a concrete jungle of neon dreams.", "Creative"),
        ("He painted his sorrow with vibrant strokes of midnight blue and crimson.", "Creative"),
        ("A single snowflake fell, a delicate masterpiece of winter's breath.", "Creative"),
        ("The abandoned castle stood as a silent guardian of ancient lore.", "Creative"),
        
        # Urgent
        ("Warning: Evacuate the building immediately! Fire alarm activated in sector 7.", "Urgent"),
        ("Please reply ASAP. The deadline is in 10 minutes and we need your approval.", "Urgent"),
        ("EMERGENCY! We are out of coffee in the breakroom. This is not a drill.", "Urgent"),
        ("Alert! Your server is down and losing traffic rapidly. Fix it now!", "Urgent"),
        ("Hurry up! The train is leaving in exactly two minutes. Run!", "Urgent"),
        ("Critical error: Database connection lost. Immediate action required.", "Urgent"),
        ("Stop what you are doing and check your email right now!", "Urgent"),
        ("Code Red! The patient's vital signs are dropping dangerously low.", "Urgent"),
        ("We need to deploy the hotfix immediately before the system crashes.", "Urgent"),
        ("Attention all units: We have a breach in sector 4. Respond immediately.", "Urgent"),
        ("Final notice: Your account will be suspended in 24 hours if payment is not received.", "Urgent"),
        ("Quick! Grab the fire extinguisher! The toaster is on fire!", "Urgent"),
        ("This is your last chance to submit the application. Do it now!", "Urgent"),
        ("System failure imminent. Please save your work and shut down immediately.", "Urgent"),
        ("Security breach detected. Lock down the facility right away.", "Urgent"),
        ("We need those reports on my desk in five minutes or the deal is off!", "Urgent"),
        ("Action required: Verify your identity immediately to prevent account lockout.", "Urgent"),
        ("Rush this order to the front of the queue. The client is furious.", "Urgent"),
        ("Danger! High voltage area. Do not enter under any circumstances.", "Urgent"),
        ("Evacuate the area immediately! A hurricane is approaching the coast.", "Urgent"),
        
        # Casual
        ("Hey man, what's up? Are we still hanging out tonight?", "Casual"),
        ("Just grabbed some pizza. It's so good! You should come over.", "Casual"),
        ("lol that meme you sent me was hilarious 😂", "Casual"),
        ("I'm so tired today. Just gonna chill and watch Netflix all evening.", "Casual"),
        ("Yeah sure, sounds good to me. See ya later!", "Casual"),
        ("Can you pick up some milk on your way home? Thanks!", "Casual"),
        ("That movie was wild, dude. We gotta see it again.", "Casual"),
        ("Are we still on for the game this weekend?", "Casual"),
        ("I can't believe how hot it is outside today. So annoying.", "Casual"),
        ("Just finished my workout. Feeling great but super exhausted.", "Casual"),
        ("Did you see what happened on the latest episode? Crazy stuff.", "Casual"),
        ("I'm starving. Let's go grab some burgers or tacos.", "Casual"),
        ("Sorry I missed your call, was in the shower. What's up?", "Casual"),
        ("That new song is stuck in my head all day.", "Casual"),
        ("Can't wait for Friday, this week has been dragging on forever.", "Casual"),
        ("Let me know when you're free to hop on a call.", "Casual"),
        ("Whoa, that's awesome! Congrats on the new job!", "Casual"),
        ("I'm just wearing sweatpants today, not trying to impress anyone.", "Casual"),
        ("Don't forget to feed the dog before you leave.", "Casual"),
        ("Haha yeah exactly, I know exactly what you mean.", "Casual")
    ]
    return pd.DataFrame(data, columns=["text", "vibe"])

def main():
    print("Generating extended synthetic dataset...")
    df = get_dataset()
    
    X = df['text']
    y = df['vibe']
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Define Pipeline
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words='english')),
        ('clf', RandomForestClassifier(random_state=42))
    ])
    
    # Hyperparameters
    param_grid = {
        'tfidf__max_features': [1000, 5000, None],
        'tfidf__ngram_range': [(1, 1), (1, 2)],
        'clf__n_estimators': [50, 100],
        'clf__max_depth': [None, 10, 20]
    }
    
    print("Starting Hyperparameter Tuning with GridSearchCV...")
    grid_search = GridSearchCV(pipeline, param_grid, cv=3, n_jobs=-1, verbose=1)
    grid_search.fit(X_train, y_train)
    
    best_model = grid_search.best_estimator_
    print(f"Best Parameters: {grid_search.best_params_}")
    
    # Evaluate
    print("Evaluating Best Model...")
    y_pred = best_model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Test Accuracy: {acc:.4f}")
    print(classification_report(y_test, y_pred))
    
    # Save artifacts
    os.makedirs("ml/runs", exist_ok=True)
    
    model_path = "ml/pipeline.pkl"
    metrics_path = "ml/runs/metrics.json"
    
    print(f"Exporting model artifact to {model_path}...")
    joblib.dump(best_model, model_path)
    
    print(f"Saving metrics to {metrics_path}...")
    metrics = {
        "timestamp": datetime.now().isoformat(),
        "best_params": grid_search.best_params_,
        "test_accuracy": acc,
        "classes": list(best_model.classes_)
    }
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=4)
        
    print("Done! Model training pipeline completed.")

if __name__ == "__main__":
    main()
