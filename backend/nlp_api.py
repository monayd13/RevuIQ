"""
RevuIQ - REAL NLP API with Transformer Models
Uses actual NLP models for sentiment analysis and text generation
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime
from sqlalchemy.orm import Session
import json

from database import get_db, Review, Business, init_db
from google_places_integration import fetch_google_reviews, get_restaurant_details

# Import NLP libraries
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch

# Initialize FastAPI
app = FastAPI(
    title="RevuIQ NLP API",
    description="Restaurant Review Management with REAL NLP",
    version="3.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== LOAD REAL NLP MODELS ====================

print("🚀 Loading NLP Models...")

# 1. Sentiment Analysis - RoBERTa (Cardiff NLP)
print("📊 Loading Sentiment Model (RoBERTa)...")
sentiment_model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model=sentiment_model_name,
    device=0 if torch.cuda.is_available() else -1
)

# 2. Emotion Detection - GoEmotions
print("😊 Loading Emotion Model (GoEmotions)...")
emotion_model_name = "SamLowe/roberta-base-go_emotions"
emotion_analyzer = pipeline(
    "text-classification",
    model=emotion_model_name,
    top_k=3,
    device=0 if torch.cuda.is_available() else -1
)

# 3. Text Generation - T5
print("✍️ Loading Response Generator (T5)...")
response_generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    device=0 if torch.cuda.is_available() else -1
)

print("✅ All NLP models loaded successfully!")

# ==================== DATA MODELS ====================

class RestaurantCreate(BaseModel):
    name: str
    industry: str = "restaurant"

class ReviewAnalysisRequest(BaseModel):
    text: str
    business_name: Optional[str] = "Restaurant"

class ReviewBulkCreate(BaseModel):
    business_id: int
    reviews: List[Dict]

# ==================== REAL NLP FUNCTIONS ====================

def analyze_sentiment_nlp(text: str) -> Dict:
    """
    Real sentiment analysis using RoBERTa transformer model
    Returns: {"label": "POSITIVE/NEUTRAL/NEGATIVE", "score": float}
    """
    try:
        result = sentiment_analyzer(text[:512])[0]  # Limit to 512 tokens
        
        # Map labels
        label_map = {
            "positive": "POSITIVE",
            "neutral": "NEUTRAL",
            "negative": "NEGATIVE",
            "LABEL_0": "NEGATIVE",
            "LABEL_1": "NEUTRAL",
            "LABEL_2": "POSITIVE"
        }
        
        return {
            "label": label_map.get(result['label'], result['label']),
            "score": round(result['score'], 3)
        }
    except Exception as e:
        print(f"Sentiment analysis error: {e}")
        return {"label": "NEUTRAL", "score": 0.5}

def detect_emotions_nlp(text: str) -> Dict:
    """
    Real emotion detection using GoEmotions model
    Returns: {"emotion1": score1, "emotion2": score2, ...}
    """
    try:
        results = emotion_analyzer(text[:512])
        emotions = {}
        
        for emotion_list in results:
            for emotion in emotion_list[:3]:  # Top 3 emotions
                emotions[emotion['label']] = round(emotion['score'], 3)
        
        return emotions
    except Exception as e:
        print(f"Emotion detection error: {e}")
        return {"neutral": 0.7}

def extract_aspects_nlp(text: str) -> List[Dict]:
    """
    Aspect extraction using keyword matching + sentiment context
    Returns: [{"aspect": "food", "sentiment": "positive"}, ...]
    """
    aspects = []
    text_lower = text.lower()
    
    # Define aspect keywords
    aspect_keywords = {
        "food": ["food", "meal", "dish", "taste", "flavor", "cuisine", "menu", "pasta", "pizza", "burger"],
        "service": ["service", "staff", "waiter", "server", "waitress", "employee", "manager"],
        "ambiance": ["atmosphere", "ambiance", "decor", "environment", "vibe", "setting", "music"],
        "price": ["price", "expensive", "cheap", "value", "cost", "worth", "affordable"],
        "cleanliness": ["clean", "dirty", "hygiene", "sanitary", "tidy"],
        "location": ["location", "parking", "access", "convenient", "area"]
    }
    
    # Check each aspect
    for aspect, keywords in aspect_keywords.items():
        if any(word in text_lower for word in keywords):
            # Use sentiment to determine aspect sentiment
            sentiment_result = analyze_sentiment_nlp(text)
            aspects.append({
                "aspect": aspect,
                "sentiment": sentiment_result["label"].lower()
            })
    
    return aspects if aspects else [{"aspect": "general", "sentiment": "positive"}]

def generate_response_nlp(text: str, sentiment: str, business_name: str = "Restaurant") -> str:
    """
    Generate response using T5 model
    Returns: AI-generated response string
    """
    try:
        # Create prompt based on sentiment
        if sentiment == "POSITIVE":
            prompt = f"Write a grateful response to this positive review: {text[:200]}"
        elif sentiment == "NEGATIVE":
            prompt = f"Write an apologetic response to this negative review: {text[:200]}"
        else:
            prompt = f"Write a polite response to this review: {text[:200]}"
        
        # Generate response
        result = response_generator(prompt, max_length=100, num_return_sequences=1)
        generated = result[0]['generated_text']
        
        # If response is too short, use template
        if len(generated) < 20:
            if sentiment == "POSITIVE":
                return f"Thank you so much for your wonderful feedback! We're thrilled you enjoyed your experience at {business_name}. We look forward to welcoming you back soon!"
            elif sentiment == "NEGATIVE":
                return f"We sincerely apologize for your experience at {business_name}. Your feedback is important to us and we're working to improve. Please contact us directly so we can make this right."
            else:
                return f"Thank you for your feedback about {business_name}! We appreciate you taking the time to share your thoughts with us."
        
        return generated
        
    except Exception as e:
        print(f"Response generation error: {e}")
        # Fallback to templates
        if sentiment == "POSITIVE":
            return f"Thank you for your wonderful review! We're delighted you enjoyed {business_name}!"
        elif sentiment == "NEGATIVE":
            return f"We apologize for your experience. Please contact us at {business_name} to make this right."
        else:
            return f"Thank you for your feedback about {business_name}!"

# ==================== HEALTH CHECK ====================

@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "RevuIQ NLP API",
        "version": "3.0.0",
        "nlp_models": {
            "sentiment": "cardiffnlp/twitter-roberta-base-sentiment-latest",
            "emotion": "SamLowe/roberta-base-go_emotions",
            "generation": "google/flan-t5-base"
        },
        "models_loaded": True
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "mode": "nlp",
        "models_loaded": True,
        "device": "cuda" if torch.cuda.is_available() else "cpu"
    }

# ==================== NLP ANALYSIS ENDPOINT ====================

@app.post("/api/analyze")
async def analyze_review(request: ReviewAnalysisRequest):
    """
    Analyze review text using REAL NLP models
    """
    try:
        start_time = datetime.now()
        
        # 1. Sentiment Analysis (RoBERTa)
        sentiment = analyze_sentiment_nlp(request.text)
        
        # 2. Emotion Detection (GoEmotions)
        emotions = detect_emotions_nlp(request.text)
        
        # 3. Aspect Extraction
        aspects = extract_aspects_nlp(request.text)
        
        # 4. Response Generation (T5)
        response = generate_response_nlp(
            request.text,
            sentiment["label"],
            request.business_name
        )
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        return {
            "success": True,
            "sentiment": sentiment["label"],
            "sentiment_score": sentiment["score"],
            "emotions": emotions,
            "aspects": aspects,
            "suggested_response": response,
            "processing_time_ms": round(processing_time, 2),
            "models_used": ["RoBERTa", "GoEmotions", "T5"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== RESTAURANT ENDPOINTS ====================

@app.post("/api/restaurants")
async def create_restaurant(restaurant: RestaurantCreate, db: Session = Depends(get_db)):
    """Create a new restaurant"""
    try:
        new_business = Business(
            name=restaurant.name,
            industry=restaurant.industry,
            created_at=datetime.utcnow()
        )
        db.add(new_business)
        db.commit()
        db.refresh(new_business)
        
        return {
            "success": True,
            "restaurant": {
                "id": new_business.id,
                "name": new_business.name,
                "industry": new_business.industry,
                "created_at": new_business.created_at.isoformat()
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/restaurants")
async def get_restaurants(db: Session = Depends(get_db)):
    """Get all restaurants"""
    try:
        businesses = db.query(Business).all()
        
        restaurants = []
        for business in businesses:
            review_count = db.query(Review).filter(Review.business_id == business.id).count()
            restaurants.append({
                "id": business.id,
                "name": business.name,
                "industry": business.industry,
                "created_at": business.created_at.isoformat(),
                "review_count": review_count
            })
        
        return {
            "success": True,
            "count": len(restaurants),
            "restaurants": restaurants
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/reviews/restaurant/{restaurant_id}")
async def get_restaurant_reviews(restaurant_id: int, db: Session = Depends(get_db)):
    """Get reviews for a specific restaurant with NLP analysis"""
    try:
        reviews = db.query(Review).filter(Review.business_id == restaurant_id).order_by(Review.review_date.desc()).all()
        
        review_list = []
        for review in reviews:
            review_list.append({
                "id": review.id,
                "platform": review.platform,
                "author": review.author_name,
                "rating": review.rating,
                "text": review.text,
                "date": review.review_date.isoformat() if review.review_date else None,
                "sentiment": review.sentiment,
                "sentiment_score": review.sentiment_score,
                "emotions": json.loads(review.emotions) if review.emotions else {},
                "aspects": json.loads(review.aspects) if review.aspects else [],
                "ai_response": review.ai_response
            })
        
        return {
            "success": True,
            "count": len(review_list),
            "reviews": review_list
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== STARTUP ====================

# Initialize database
init_db()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
