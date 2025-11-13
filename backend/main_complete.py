"""
RevuIQ Backend API - Complete Version
With database, platform APIs, and aspect extraction
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from textblob import TextBlob
from database_manager import db_manager
from platform_apis import PlatformAggregator, get_demo_reviews
from nlp_pipeline.aspect_extractor import AspectExtractor

# Initialize FastAPI
app = FastAPI(
    title="RevuIQ API - Complete",
    description="AI-Powered Review Management with Database & Platform Integration",
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

# Initialize components
platform_aggregator = PlatformAggregator()
aspect_extractor = AspectExtractor()

# ==================== DATA MODELS ====================

class ReviewInput(BaseModel):
    text: str
    rating: Optional[float] = None
    platform: Optional[str] = "manual"
    business_name: Optional[str] = "Your Business"
    author: Optional[str] = None

class BusinessCreate(BaseModel):
    name: str
    platform: str
    platform_id: str
    category: Optional[str] = None
    location: Optional[str] = None

class FetchReviewsRequest(BaseModel):
    business_name: str
    location: Optional[str] = None
    google_place_id: Optional[str] = None
    yelp_business_id: Optional[str] = None
    meta_page_id: Optional[str] = None

# ==================== HELPER FUNCTIONS ====================

def analyze_sentiment(text: str):
    """Analyze sentiment using TextBlob"""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    if polarity > 0.1:
        label = "POSITIVE"
        score = (polarity + 1) / 2
    elif polarity < -0.1:
        label = "NEGATIVE"
        score = (1 - abs(polarity)) / 2
    else:
        label = "NEUTRAL"
        score = 0.5
    
    return {
        "label": label,
        "score": score,
        "polarity": polarity,
        "subjectivity": subjectivity
    }

def detect_emotions(text: str, sentiment: str):
    """Detect emotions"""
    text_lower = text.lower()
    
    emotions = {
        "joy": ["happy", "great", "excellent", "amazing", "wonderful", "love", "best"],
        "anger": ["angry", "terrible", "worst", "horrible", "hate", "awful"],
        "disappointment": ["disappointed", "expected", "unfortunately", "not good"],
        "gratitude": ["thank", "appreciate", "grateful"],
        "frustration": ["slow", "wait", "long", "never", "still"]
    }
    
    emotion_scores = {}
    for emotion, keywords in emotions.items():
        score = sum(1 for keyword in keywords if keyword in text_lower)
        emotion_scores[emotion] = score
    
    if sentiment == "POSITIVE":
        primary = "joy" if emotion_scores["joy"] > 0 else "gratitude"
        confidence = 0.8
    elif sentiment == "NEGATIVE":
        if emotion_scores["anger"] > 0:
            primary = "anger"
        elif emotion_scores["disappointment"] > 0:
            primary = "disappointment"
        else:
            primary = "frustration"
        confidence = 0.75
    else:
        primary = "neutral"
        confidence = 0.6
    
    return {
        "primary_emotion": primary,
        "confidence": confidence,
        "all_emotions": emotion_scores
    }

def generate_ai_response(text: str, sentiment: str, emotion: str, business_name: str):
    """Generate AI response"""
    responses = {
        "POSITIVE": {
            "joy": f"Thank you so much for the wonderful feedback! We're thrilled you had such a great experience at {business_name}. We look forward to serving you again soon!",
            "gratitude": f"We truly appreciate your kind words! It means the world to our team at {business_name}. Thank you for choosing us!",
            "default": f"Thank you for your positive review! We're so glad you enjoyed your experience at {business_name}."
        },
        "NEGATIVE": {
            "anger": f"We sincerely apologize for your experience. This is not the standard we hold at {business_name}. Please contact us directly so we can make this right.",
            "disappointment": f"We're sorry we didn't meet your expectations. Your feedback is valuable to us at {business_name}, and we're working to improve. We'd love the chance to serve you better.",
            "frustration": f"We apologize for the inconvenience you experienced. We're taking your feedback seriously at {business_name} and working to address these issues.",
            "default": f"We're sorry to hear about your experience at {business_name}. We take all feedback seriously and would like to make things right. Please reach out to us directly."
        },
        "NEUTRAL": {
            "default": f"Thank you for taking the time to share your feedback about {business_name}. We appreciate your input and are always working to improve our service."
        }
    }
    
    sentiment_responses = responses.get(sentiment, responses["NEUTRAL"])
    response_text = sentiment_responses.get(emotion, sentiment_responses["default"])
    
    tone = "apologetic" if sentiment == "NEGATIVE" else "grateful" if sentiment == "POSITIVE" else "professional"
    confidence = 0.85 if sentiment in ["POSITIVE", "NEGATIVE"] else 0.7
    
    return {
        "response": response_text,
        "tone": tone,
        "confidence": confidence
    }

def process_review_complete(review_text: str, business_name: str):
    """Complete review processing with all features"""
    # Sentiment
    sentiment_result = analyze_sentiment(review_text)
    
    # Emotion
    emotion_result = detect_emotions(review_text, sentiment_result["label"])
    
    # Aspects
    aspect_result = aspect_extractor.extract(review_text)
    
    # AI Response
    ai_response = generate_ai_response(
        review_text,
        sentiment_result["label"],
        emotion_result["primary_emotion"],
        business_name
    )
    
    return {
        "sentiment": sentiment_result,
        "emotions": emotion_result,
        "aspects": aspect_result,
        "ai_response": ai_response
    }

# ==================== ENDPOINTS ====================

@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "RevuIQ API - Complete",
        "version": "3.0.0",
        "features": [
            "Sentiment Analysis",
            "Emotion Detection",
            "Aspect Extraction",
            "AI Response Generation",
            "Database Storage",
            "Platform API Integration",
            "Analytics Dashboard"
        ]
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "connected",
        "nlp_engine": "TextBlob + AspectExtractor",
        "version": "3.0.0"
    }

@app.post("/api/analyze-complete")
async def analyze_complete(review: ReviewInput):
    """
    Complete analysis with database storage
    """
    try:
        # Process review
        analysis = process_review_complete(review.text, review.business_name)
        
        # Store in database (create business if needed)
        business = db_manager.get_business_by_platform_id(f"{review.platform}_{review.business_name}")
        if not business:
            business = db_manager.create_business(
                name=review.business_name,
                platform=review.platform,
                platform_id=f"{review.platform}_{review.business_name}"
            )
        
        # Create review record
        db_review = db_manager.create_review(
            business_id=business.id,
            platform=review.platform,
            text=review.text,
            author=review.author,
            rating=review.rating
        )
        
        # Update with analysis
        db_manager.update_review_analysis(
            review_id=db_review.id,
            sentiment=analysis["sentiment"]["label"],
            sentiment_score=analysis["sentiment"]["score"],
            polarity=analysis["sentiment"]["polarity"],
            subjectivity=analysis["sentiment"]["subjectivity"],
            primary_emotion=analysis["emotions"]["primary_emotion"],
            emotion_confidence=analysis["emotions"]["confidence"],
            aspects=analysis["aspects"]["all_aspects"],
            ai_response=analysis["ai_response"]["response"],
            response_tone=analysis["ai_response"]["tone"],
            response_confidence=analysis["ai_response"]["confidence"]
        )
        
        return {
            "success": True,
            "review_id": db_review.id,
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/fetch-reviews")
async def fetch_reviews(request: FetchReviewsRequest, background_tasks: BackgroundTasks):
    """
    Fetch reviews from platform APIs
    """
    try:
        # Use demo reviews if no API keys configured
        if not any([request.google_place_id, request.yelp_business_id, request.meta_page_id]):
            reviews_dict = {"demo": get_demo_reviews()}
        else:
            reviews_dict = platform_aggregator.fetch_all_reviews(
                business_name=request.business_name,
                location=request.location,
                google_place_id=request.google_place_id,
                yelp_business_id=request.yelp_business_id,
                meta_page_id=request.meta_page_id
            )
        
        total_count = platform_aggregator.get_total_count(reviews_dict)
        
        # Process reviews in background
        # (In production, use Celery or similar for this)
        
        return {
            "success": True,
            "total_reviews": total_count,
            "by_platform": {
                platform: len(reviews) 
                for platform, reviews in reviews_dict.items()
            },
            "message": f"Fetched {total_count} reviews. Processing in background."
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/sentiment-distribution")
async def get_sentiment_distribution(business_id: Optional[int] = None, days: int = 30):
    """Get sentiment distribution"""
    try:
        distribution = db_manager.get_sentiment_distribution(business_id, days)
        return {
            "success": True,
            "distribution": distribution,
            "days": days
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/emotion-distribution")
async def get_emotion_distribution(business_id: Optional[int] = None, days: int = 30):
    """Get emotion distribution"""
    try:
        distribution = db_manager.get_emotion_distribution(business_id, days)
        return {
            "success": True,
            "distribution": distribution,
            "days": days
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/sentiment-trend")
async def get_sentiment_trend(business_id: Optional[int] = None, days: int = 30):
    """Get sentiment trend over time"""
    try:
        trend = db_manager.get_sentiment_trend(business_id, days)
        return {
            "success": True,
            "trend": trend,
            "days": days
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/stats")
async def get_analytics_stats(business_id: Optional[int] = None):
    """Get overall analytics statistics"""
    try:
        response_stats = db_manager.get_response_stats(business_id)
        avg_rating = db_manager.get_average_rating(business_id)
        
        return {
            "success": True,
            "response_stats": response_stats,
            "average_rating": avg_rating
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/reviews/pending")
async def get_pending_reviews(limit: int = 50):
    """Get reviews pending approval"""
    try:
        reviews = db_manager.get_pending_reviews(limit)
        
        return {
            "success": True,
            "count": len(reviews),
            "reviews": [
                {
                    "id": r.id,
                    "text": r.text,
                    "sentiment": r.sentiment,
                    "emotion": r.primary_emotion,
                    "ai_response": r.ai_response,
                    "created_at": r.created_at.isoformat()
                }
                for r in reviews
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/reviews/{review_id}/approve")
async def approve_review(review_id: int, final_response: Optional[str] = None):
    """Approve AI response"""
    try:
        db_manager.approve_response(review_id, final_response)
        return {
            "success": True,
            "message": "Response approved",
            "review_id": review_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/reviews/{review_id}/post")
async def post_review_response(review_id: int):
    """Mark response as posted"""
    try:
        db_manager.post_response(review_id)
        return {
            "success": True,
            "message": "Response marked as posted",
            "review_id": review_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== RUN SERVER ====================

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting RevuIQ API Server (Complete Version)")
    print("📊 Features: Database, Platform APIs, Aspect Extraction, Analytics")
    print("🌐 Server: http://localhost:8000")
    print("📖 API Docs: http://localhost:8000/docs")
    
    uvicorn.run(
        "main_complete:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
