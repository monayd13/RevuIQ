"""
RevuIQ Backend API - Production Ready
FastAPI server with TextBlob for reliable NLP
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import os
import sys

from textblob import TextBlob

# Add modules to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'nlp_pipeline'))

try:
    from simple_google_reviews import GoogleReviewsFetcher
    google_fetcher = GoogleReviewsFetcher()
except:
    google_fetcher = None

try:
    from yelp_reviews import YelpReviewsFetcher
    yelp_fetcher = YelpReviewsFetcher()
    print("✅ Yelp API loaded! (FREE - No credit card needed)")
except:
    yelp_fetcher = None
    print("⚠️  Yelp API not available")

# Try to load RAG system (optional, free upgrade)
try:
    from rag_system import ReviewRAG
    rag_system = ReviewRAG()
    RAG_AVAILABLE = True
    print("✅ RAG System loaded! (Free semantic search enabled)")
except Exception as e:
    rag_system = None
    RAG_AVAILABLE = False
    print(f"⚠️  RAG not available: {e}")
    print("   Install with: pip install sentence-transformers chromadb")

# Initialize FastAPI app
app = FastAPI(
    title="RevuIQ API",
    description="AI-Powered Review Management System",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== DATA MODELS ====================

class ReviewInput(BaseModel):
    """Input review for analysis"""
    text: str
    rating: Optional[float] = None
    platform: Optional[str] = "unknown"
    business_name: Optional[str] = "Your Business"

class SentimentResult(BaseModel):
    """Sentiment analysis result"""
    label: str  # POSITIVE, NEGATIVE, NEUTRAL
    score: float
    polarity: float
    subjectivity: float

class EmotionResult(BaseModel):
    """Emotion detection result"""
    primary_emotion: str
    confidence: float
    all_emotions: dict

class AIResponse(BaseModel):
    """AI-generated response"""
    response: str
    tone: str
    confidence: float

class AnalysisResponse(BaseModel):
    """Complete analysis response"""
    success: bool
    sentiment: SentimentResult
    emotions: EmotionResult
    ai_response: AIResponse
    timestamp: str

# ==================== HELPER FUNCTIONS ====================

def analyze_sentiment(text: str) -> SentimentResult:
    """Analyze sentiment using TextBlob"""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    # Stricter thresholds for better neutral detection
    if polarity > 0.25:
        label = "POSITIVE"
        score = (polarity + 1) / 2  # Convert to 0-1 scale
    elif polarity < -0.25:
        label = "NEGATIVE"
        score = (1 - abs(polarity)) / 2
    else:
        label = "NEUTRAL"
        score = 0.5 + (polarity * 0.5)  # Slight variation for neutral
    
    return SentimentResult(
        label=label,
        score=score,
        polarity=polarity,
        subjectivity=subjectivity
    )

def detect_emotions(text: str, sentiment: str) -> EmotionResult:
    """Detect emotions based on sentiment and keywords"""
    text_lower = text.lower()
    
    # Emotion keywords
    emotions = {
        "joy": ["happy", "great", "excellent", "amazing", "wonderful", "love", "best"],
        "anger": ["angry", "terrible", "worst", "horrible", "hate", "awful"],
        "disappointment": ["disappointed", "expected", "unfortunately", "not good"],
        "gratitude": ["thank", "appreciate", "grateful"],
        "frustration": ["slow", "wait", "long", "never", "still"]
    }
    
    # Count emotion keywords
    emotion_scores = {}
    for emotion, keywords in emotions.items():
        score = sum(1 for keyword in keywords if keyword in text_lower)
        emotion_scores[emotion] = score
    
    # Determine primary emotion
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
    
    return EmotionResult(
        primary_emotion=primary,
        confidence=confidence,
        all_emotions=emotion_scores
    )

def generate_ai_response(text: str, sentiment: str, emotion: str, business_name: str) -> AIResponse:
    """Generate appropriate response based on sentiment and emotion"""
    
    # Try RAG-based response first (better, context-aware)
    if RAG_AVAILABLE and rag_system:
        try:
            response_text = rag_system.generate_response(text, sentiment, business_name)
            tone = "apologetic" if sentiment == "NEGATIVE" else "grateful" if sentiment == "POSITIVE" else "professional"
            return AIResponse(
                response=response_text,
                tone=tone,
                confidence=0.90  # Higher confidence with RAG
            )
        except Exception as e:
            print(f"⚠️  RAG response failed, using fallback: {e}")
    
    # Fallback to template-based responses
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
    
    # Get appropriate response
    sentiment_responses = responses.get(sentiment, responses["NEUTRAL"])
    response_text = sentiment_responses.get(emotion, sentiment_responses["default"])
    
    tone = "apologetic" if sentiment == "NEGATIVE" else "grateful" if sentiment == "POSITIVE" else "professional"
    confidence = 0.85 if sentiment in ["POSITIVE", "NEGATIVE"] else 0.7
    
    return AIResponse(
        response=response_text,
        tone=tone,
        confidence=confidence
    )

# ==================== API ENDPOINTS ====================

@app.get("/")
async def root():
    """API health check"""
    return {
        "status": "online",
        "service": "RevuIQ API",
        "version": "2.0.0",
        "message": "AI-Powered Review Management System",
        "endpoints": {
            "analyze": "/api/analyze",
            "bulk_analyze": "/api/bulk-analyze",
            "health": "/health",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "nlp_engine": "TextBlob",
        "version": "2.0.0",
        "ready": True
    }

@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_review(review: ReviewInput):
    """
    Analyze a single review
    """
    try:
        sentiment_result = analyze_sentiment(review.text)
        emotion_result = detect_emotions(review.text, sentiment_result.label)
        ai_response = generate_ai_response(
            review.text,
            sentiment_result.label,
            emotion_result.primary_emotion,
            review.business_name
        )
        
        # Store in RAG system for future context (if available)
        if RAG_AVAILABLE and rag_system:
            try:
                rag_system.add_review(review.text, {
                    'sentiment': sentiment_result.label,
                    'rating': review.rating,
                    'business': review.business_name,
                    'platform': review.platform
                })
            except Exception as e:
                print(f"⚠️  Failed to store in RAG: {e}")
        
        return {
            "success": True,
            "sentiment": sentiment_result.dict(),
            "emotions": emotion_result.dict(),
            "ai_response": ai_response.dict(),
            "rag_enabled": RAG_AVAILABLE,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/bulk-analyze")
async def bulk_analyze(reviews: List[ReviewInput]):
    """
    Analyze multiple reviews at once
    Returns analysis for all reviews
    """
    try:
        results = []
        
        for review in reviews:
            sentiment_result = analyze_sentiment(review.text)
            emotion_result = detect_emotions(review.text, sentiment_result.label)
            ai_response = generate_ai_response(
                review.text,
                sentiment_result.label,
                emotion_result.primary_emotion,
                review.business_name
            )
            
            results.append({
                "text": review.text,
                "sentiment": sentiment_result.dict(),
                "emotions": emotion_result.dict(),
                "ai_response": ai_response.dict()
            })
        
        return {
            "success": True,
            "count": len(results),
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bulk analysis failed: {str(e)}")

@app.post("/api/fetch-reviews")
async def fetch_reviews(business_name: str, location: Optional[str] = None, platform: str = "yelp"):
    """
    Fetch reviews from Yelp (FREE) or Google Places API
    Platform options: 'yelp' (default, FREE), 'google'
    """
    try:
        # Try Yelp first (FREE - No credit card!)
        if platform == "yelp" and yelp_fetcher and yelp_fetcher.api_key:
            print(f"🔍 Fetching real reviews from Yelp for: {business_name}")
            reviews = yelp_fetcher.fetch_business_reviews(business_name, location or "")
            mode = "real"
            note = "Fetched from Yelp Fusion API (FREE)"
        # Fallback to Google
        elif platform == "google" and google_fetcher and google_fetcher.api_key:
            print(f"🔍 Fetching real reviews from Google for: {business_name}")
            reviews = google_fetcher.fetch_restaurant_reviews(business_name, location or "")
            mode = "real"
            note = "Fetched from Google Places API"
        else:
            print(f"⚠️  No API key - using demo reviews")
            reviews = yelp_fetcher._get_demo_reviews() if yelp_fetcher else []
            mode = "demo"
            note = "Demo mode - Add YELP_API_KEY to .env for FREE real reviews (no credit card!)"
        
        # Count by platform
        platform_counts = {}
        for review in reviews:
            platform = review.get("platform", "Unknown")
            platform_counts[platform] = platform_counts.get(platform, 0) + 1
        
        return {
            "success": True,
            "total_reviews": len(reviews),
            "reviews": reviews,
            "by_platform": platform_counts,
            "message": f"Fetched {len(reviews)} reviews for {business_name}",
            "mode": mode,
            "note": note
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/search-similar")
async def search_similar_reviews(query: str, n_results: int = 5, sentiment_filter: Optional[str] = None):
    """
    Search for similar reviews using semantic search (RAG)
    """
    if not RAG_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="RAG system not available. Install with: pip install sentence-transformers chromadb"
        )
    
    try:
        similar = rag_system.find_similar_reviews(query, n_results, sentiment_filter)
        return {
            "success": True,
            "query": query,
            "results": similar,
            "count": len(similar)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/rag-stats")
async def get_rag_stats():
    """Get RAG database statistics"""
    if not RAG_AVAILABLE:
        return {
            "rag_available": False,
            "message": "Install with: pip install sentence-transformers chromadb"
        }
    
    try:
        stats = rag_system.get_stats()
        return {
            "rag_available": True,
            "stats": stats
        }
    except Exception as e:
        return {
            "rag_available": False,
            "error": str(e)
        }

@app.get("/api/stats")
async def get_stats():
    """Get API statistics"""
    features = [
        "Sentiment Analysis",
        "Emotion Detection",
        "AI Response Generation",
        "Bulk Processing",
        "Fetch Reviews (Demo)"
    ]
    
    if RAG_AVAILABLE:
        features.append("RAG Semantic Search (Free)")
        features.append("Context-Aware Responses")
    
    return {
        "version": "2.0.0",
        "nlp_engine": "TextBlob + RAG" if RAG_AVAILABLE else "TextBlob",
        "status": "operational",
        "rag_enabled": RAG_AVAILABLE,
        "features": features,
        "timestamp": datetime.now().isoformat()
    }

# ==================== RUN SERVER ====================

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting RevuIQ API Server (Production)")
    print("📊 NLP Engine: TextBlob (Fast & Reliable)")
    print("🌐 Server: http://localhost:8000")
    print("📖 API Docs: http://localhost:8000/docs")
    print("📊 Reviews Dashboard: http://localhost:3000/reviews")
    
    uvicorn.run(
        "main_production:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
