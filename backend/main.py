"""
RevuIQ Backend API
FastAPI server for AI-powered review management
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime, timedelta
import uvicorn
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nlp_pipeline.sentiment_analyzer import SentimentAnalyzer
from nlp_pipeline.emotion_detector import EmotionDetector
from nlp_pipeline.response_generator import ResponseGenerator

# Initialize FastAPI app
app = FastAPI(
    title="RevuIQ API",
    description="AI-Powered Review Management System",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Initialize NLP models (lazy loading)
sentiment_analyzer = None
emotion_detector = None
response_generator = None

def get_sentiment_analyzer():
    global sentiment_analyzer
    if sentiment_analyzer is None:
        sentiment_analyzer = SentimentAnalyzer()
    return sentiment_analyzer

def get_emotion_detector():
    global emotion_detector
    if emotion_detector is None:
        emotion_detector = EmotionDetector()
    return emotion_detector

def get_response_generator():
    global response_generator
    if response_generator is None:
        response_generator = ResponseGenerator()
    return response_generator


# ==================== DATA MODELS ====================

class Review(BaseModel):
    """Review data model"""
    id: Optional[int] = None
    platform: str  # google, yelp, tripadvisor, meta
    review_id: str
    author: str
    rating: float
    text: str
    date: datetime
    business_id: str
    
class ReviewAnalysis(BaseModel):
    """Review analysis result"""
    review_id: str
    sentiment: dict
    emotions: dict
    aspects: Optional[List[str]] = None
    ai_response: Optional[str] = None
    
class ResponseRequest(BaseModel):
    """Request for AI response generation"""
    review_text: str
    sentiment: Optional[str] = None
    business_name: Optional[str] = None
    tone: Optional[str] = "professional"  # professional, friendly, apologetic
    
class BulkAnalysisRequest(BaseModel):
    """Request for bulk review analysis"""
    reviews: List[dict]


# ==================== HEALTH CHECK ====================

@app.get("/")
async def root():
    """API health check"""
    return {
        "status": "online",
        "service": "RevuIQ API",
        "version": "1.0.0",
        "endpoints": {
            "analyze": "/api/analyze",
            "generate_response": "/api/generate-response",
            "bulk_analyze": "/api/bulk-analyze",
            "stats": "/api/stats"
        }
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "models": {
            "sentiment_analyzer": sentiment_analyzer is not None,
            "emotion_detector": emotion_detector is not None,
            "response_generator": response_generator is not None
        }
    }


# ==================== NLP ENDPOINTS ====================

@app.post("/api/analyze")
async def analyze_review(review: dict):
    """
    Analyze a single review
    
    Returns sentiment, emotions, and aspects
    """
    try:
        text = review.get("text", "")
        if not text:
            raise HTTPException(status_code=400, detail="Review text is required")
        
        # Get analyzers
        sentiment = get_sentiment_analyzer()
        emotion = get_emotion_detector()
        
        # Perform analysis
        sentiment_result = sentiment.analyze(text)
        emotion_result = emotion.detect(text)
        
        return {
            "success": True,
            "review_id": review.get("id", "unknown"),
            "sentiment": sentiment_result,
            "emotions": emotion_result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate-response")
async def generate_response(request: ResponseRequest):
    """
    Generate AI response for a review
    
    Returns a professional, empathetic response
    """
    try:
        generator = get_response_generator()
        
        # Generate response
        response = generator.generate(
            review_text=request.review_text,
            sentiment=request.sentiment,
            business_name=request.business_name,
            tone=request.tone
        )
        
        return {
            "success": True,
            "ai_response": response,
            "tone": request.tone,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/bulk-analyze")
async def bulk_analyze(request: BulkAnalysisRequest):
    """
    Analyze multiple reviews at once
    
    Returns analysis for all reviews
    """
    try:
        sentiment = get_sentiment_analyzer()
        emotion = get_emotion_detector()
        
        results = []
        for review in request.reviews:
            text = review.get("text", "")
            if text:
                sentiment_result = sentiment.analyze(text)
                emotion_result = emotion.detect(text)
                
                results.append({
                    "review_id": review.get("id", "unknown"),
                    "sentiment": sentiment_result,
                    "emotions": emotion_result
                })
        
        return {
            "success": True,
            "count": len(results),
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats")
async def get_stats():
    """
    Get API statistics and model info
    """
    return {
        "total_requests": 0,  # TODO: Implement request counting
        "models_loaded": {
            "sentiment": sentiment_analyzer is not None,
            "emotion": emotion_detector is not None,
            "response": response_generator is not None
        },
        "uptime": "N/A",  # TODO: Implement uptime tracking
        "version": "1.0.0"
    }


# ==================== RUN SERVER ====================

if __name__ == "__main__":
    print("🚀 Starting RevuIQ API Server...")
    print("📊 Loading NLP models (this may take a moment)...")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
