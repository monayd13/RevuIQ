"""
RevuIQ - REAL NLP API (Simple Loading)
Uses actual NLP models - loads on first request to avoid threading issues
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

# Global variables for models (loaded on first use)
_sentiment_analyzer = None
_emotion_analyzer = None
_response_generator = None

# ==================== LAZY LOAD NLP MODELS ====================

def get_sentiment_analyzer():
    """Lazy load sentiment model"""
    global _sentiment_analyzer
    if _sentiment_analyzer is None:
        print("📊 Loading Sentiment Model (RoBERTa)...")
        from transformers import pipeline
        import torch
        _sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment-latest",
            device=-1  # CPU only to avoid threading issues
        )
        print("✅ Sentiment model loaded!")
    return _sentiment_analyzer

def get_emotion_analyzer():
    """Lazy load emotion model"""
    global _emotion_analyzer
    if _emotion_analyzer is None:
        print("😊 Loading Emotion Model (GoEmotions)...")
        from transformers import pipeline
        import torch
        _emotion_analyzer = pipeline(
            "text-classification",
            model="SamLowe/roberta-base-go_emotions",
            top_k=3,
            device=-1  # CPU only
        )
        print("✅ Emotion model loaded!")
    return _emotion_analyzer

def get_response_generator():
    """Lazy load response generator"""
    global _response_generator
    if _response_generator is None:
        print("✍️ Loading Response Generator (T5)...")
        from transformers import pipeline
        import torch
        _response_generator = pipeline(
            "text2text-generation",
            model="google/flan-t5-small",  # Use small model for speed
            device=-1  # CPU only
        )
        print("✅ Response generator loaded!")
    return _response_generator

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
    """Real sentiment analysis using RoBERTa"""
    try:
        analyzer = get_sentiment_analyzer()
        result = analyzer(text[:512])[0]
        
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
        print(f"Sentiment error: {e}")
        return {"label": "NEUTRAL", "score": 0.5}

def detect_emotions_nlp(text: str) -> Dict:
    """Real emotion detection using GoEmotions"""
    try:
        analyzer = get_emotion_analyzer()
        results = analyzer(text[:512])
        emotions = {}
        
        for emotion_list in results:
            for emotion in emotion_list[:3]:
                emotions[emotion['label']] = round(emotion['score'], 3)
        
        return emotions
    except Exception as e:
        print(f"Emotion error: {e}")
        return {"neutral": 0.7}

def extract_aspects_nlp(text: str) -> List[Dict]:
    """Aspect extraction with keyword matching"""
    aspects = []
    text_lower = text.lower()
    
    aspect_keywords = {
        "food": ["food", "meal", "dish", "taste", "flavor"],
        "service": ["service", "staff", "waiter", "server"],
        "ambiance": ["atmosphere", "ambiance", "decor"],
        "price": ["price", "expensive", "cheap", "value"]
    }
    
    for aspect, keywords in aspect_keywords.items():
        if any(word in text_lower for word in keywords):
            sentiment_result = analyze_sentiment_nlp(text)
            aspects.append({
                "aspect": aspect,
                "sentiment": sentiment_result["label"].lower()
            })
    
    return aspects if aspects else [{"aspect": "general", "sentiment": "positive"}]

def generate_response_nlp(text: str, sentiment: str, business_name: str = "Restaurant") -> str:
    """Generate response using T5"""
    try:
        generator = get_response_generator()
        
        if sentiment == "POSITIVE":
            prompt = f"Write a thank you response: {text[:100]}"
        elif sentiment == "NEGATIVE":
            prompt = f"Write an apology: {text[:100]}"
        else:
            prompt = f"Write a response: {text[:100]}"
        
        result = generator(prompt, max_length=60)
        generated = result[0]['generated_text']
        
        if len(generated) < 20:
            if sentiment == "POSITIVE":
                return f"Thank you for your wonderful review! We're delighted you enjoyed {business_name}!"
            elif sentiment == "NEGATIVE":
                return f"We apologize for your experience. Please contact us to make this right."
            else:
                return f"Thank you for your feedback about {business_name}!"
        
        return generated
        
    except Exception as e:
        print(f"Generation error: {e}")
        if sentiment == "POSITIVE":
            return "Thank you for your wonderful review!"
        elif sentiment == "NEGATIVE":
            return "We apologize and will work to improve."
        else:
            return "Thank you for your feedback!"

# ==================== HEALTH CHECK ====================

@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "RevuIQ NLP API",
        "version": "3.0.0",
        "nlp_models": {
            "sentiment": "RoBERTa (cardiffnlp)",
            "emotion": "GoEmotions (SamLowe)",
            "generation": "T5 (google/flan-t5-small)"
        },
        "models_loaded": _sentiment_analyzer is not None
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "mode": "nlp",
        "sentiment_loaded": _sentiment_analyzer is not None,
        "emotion_loaded": _emotion_analyzer is not None,
        "generator_loaded": _response_generator is not None
    }

# ==================== NLP ANALYSIS ENDPOINT ====================

@app.post("/api/analyze")
async def analyze_review(request: ReviewAnalysisRequest):
    """Analyze review using REAL NLP models"""
    try:
        start_time = datetime.now()
        
        # Real NLP analysis
        sentiment = analyze_sentiment_nlp(request.text)
        emotions = detect_emotions_nlp(request.text)
        aspects = extract_aspects_nlp(request.text)
        response = generate_response_nlp(request.text, sentiment["label"], request.business_name)
        
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        return {
            "success": True,
            "sentiment": sentiment["label"],
            "sentiment_score": sentiment["score"],
            "emotions": emotions,
            "aspects": aspects,
            "suggested_response": response,
            "processing_time_ms": round(processing_time, 2),
            "models_used": ["RoBERTa", "GoEmotions", "T5"],
            "nlp_powered": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== RESTAURANT ENDPOINTS ====================

@app.post("/api/restaurants")
async def create_restaurant(restaurant: RestaurantCreate, db: Session = Depends(get_db)):
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
                "name": new_business.name
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/restaurants")
async def get_restaurants(db: Session = Depends(get_db)):
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

# Initialize database
init_db()

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting NLP API...")
    print("📊 Models will load on first request")
    uvicorn.run(app, host="0.0.0.0", port=8000)
