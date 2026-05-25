"""
RevuIQ Backend API
FastAPI server for AI-powered review management
Single canonical entry point - consolidates all API functionality
"""

import logging
import json
import os
import sys
from datetime import datetime, timedelta
from typing import List, Optional, Dict

from fastapi import FastAPI, HTTPException, Depends, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import func
from sqlalchemy.orm import Session

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

import uvicorn

# ==================== LOGGING ====================

logging.basicConfig(
    level=logging.INFO,
    format='{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
)
logger = logging.getLogger(__name__)

# ==================== PATH SETUP ====================

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ==================== RATE LIMITER ====================

limiter = Limiter(key_func=get_remote_address)

# ==================== APP INIT ====================

app = FastAPI(
    title="RevuIQ API",
    description="AI-Powered Review Management System",
    version="1.0.0"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ==================== CORS ====================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3005",
        "https://revuiq.vercel.app",
        "https://revuiq-production.up.railway.app",
        os.getenv("FRONTEND_URL", ""),
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== AUTH ====================

security = HTTPBearer()

# ==================== DATABASE (optional, graceful fallback) ====================

try:
    from database import get_db, Review, Business, init_db
    init_db()
    DB_AVAILABLE = True
    logger.info("Database initialized successfully")
except Exception as e:
    DB_AVAILABLE = False
    logger.warning("Database not available: %s", e)
    get_db = None
    Review = None
    Business = None

# ==================== NLP (optional, graceful fallback) ====================

try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    from textblob import TextBlob
    vader_analyzer = SentimentIntensityAnalyzer()
    NLP_AVAILABLE = True
    logger.info("NLP engine (VADER + TextBlob) loaded successfully")
except Exception as e:
    vader_analyzer = None
    NLP_AVAILABLE = False
    logger.warning("NLP engine not available: %s", e)

# ==================== GOOGLE PLACES (optional) ====================

try:
    from google_places_integration import fetch_google_reviews, get_restaurant_details
    GOOGLE_AVAILABLE = True
except Exception:
    GOOGLE_AVAILABLE = False
    fetch_google_reviews = None
    get_restaurant_details = None

# ==================== DATA MODELS ====================

class AnalyzeRequest(BaseModel):
    """Single review analysis request"""
    text: str = Field(..., min_length=1, max_length=5000)
    business_name: Optional[str] = Field(None, max_length=200)
    rating: Optional[float] = None
    platform: Optional[str] = Field("unknown", max_length=100)


class BulkAnalysisRequest(BaseModel):
    """Bulk review analysis request"""
    reviews: List[AnalyzeRequest]


class GenerateResponseRequest(BaseModel):
    """Request for AI response generation"""
    review_text: str = Field(..., min_length=1, max_length=5000)
    sentiment: Optional[str] = None
    business_name: Optional[str] = Field(None, max_length=200)
    tone: Optional[str] = Field("professional", max_length=50)


class RestaurantCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    industry: str = Field("restaurant", max_length=100)


class ReviewCreate(BaseModel):
    platform: str = Field(..., max_length=100)
    platform_review_id: str = Field(..., max_length=200)
    business_id: int
    author_name: str = Field(..., max_length=200)
    rating: float
    text: str = Field(..., min_length=1, max_length=5000)
    review_date: datetime


class ReviewBulkCreate(BaseModel):
    business_id: int
    reviews: List[Dict]


class ApprovalRequest(BaseModel):
    is_genuine: bool
    notes: Optional[str] = Field("", max_length=1000)


class ResponseApprovalRequest(BaseModel):
    approved: bool
    edited_response: Optional[str] = Field(None, max_length=5000)


class GooglePlacesRequest(BaseModel):
    restaurant_name: str = Field(..., min_length=1, max_length=200)
    location: Optional[str] = Field("", max_length=200)
    business_id: int


# ==================== NLP HELPERS ====================

def analyze_sentiment(text: str, rating: Optional[float] = None) -> Dict:
    """Analyze sentiment using VADER (with TextBlob fallback)"""
    if not NLP_AVAILABLE:
        # Minimal mock when no NLP available
        return {"label": "NEUTRAL", "score": 0.5, "polarity": 0.0}

    try:
        text_lower = text.lower()

        strong_negative_phrases = [
            "passive aggressive", "self-righteous", "rude", "terrible", "worst",
            "horrible", "awful", "disgusting", "never again", "waste", "scam",
            "fraud", "disappointed", "disappointing"
        ]
        has_strong_negative = any(phrase in text_lower for phrase in strong_negative_phrases)

        scores = vader_analyzer.polarity_scores(text)
        compound = scores["compound"]

        if rating is not None and rating <= 2.0 and compound >= 0:
            compound = -0.5

        if has_strong_negative and compound > -0.3:
            compound = min(compound - 0.4, -0.3)

        if compound >= 0.05:
            label = "POSITIVE"
            score = min(0.5 + (compound * 0.5), 0.99)
        elif compound <= -0.05:
            label = "NEGATIVE"
            score = min(0.5 + (abs(compound) * 0.5), 0.99)
        else:
            label = "NEUTRAL"
            score = 0.5

        return {
            "label": label,
            "score": round(score, 3),
            "polarity": round(compound, 3),
            "pos": round(scores["pos"], 3),
            "neg": round(scores["neg"], 3),
            "neu": round(scores["neu"], 3),
        }
    except Exception as e:
        logger.error("Sentiment analysis error: %s", e)
        return {"label": "NEUTRAL", "score": 0.5, "polarity": 0.0}


def detect_emotions(text: str, sentiment_label: str) -> Dict:
    """Detect emotions using keyword analysis combined with VADER intensity"""
    if not NLP_AVAILABLE:
        return {"neutral": 0.7}

    emotions: Dict[str, float] = {}
    text_lower = text.lower()

    try:
        vader_scores = vader_analyzer.polarity_scores(text)
        intensity = abs(vader_scores["compound"])
    except Exception:
        intensity = 0.5

    if sentiment_label == "POSITIVE":
        if any(w in text_lower for w in ["love", "amazing", "excellent", "perfect", "best", "wonderful"]):
            emotions["joy"] = min(0.75 + (intensity * 0.20), 0.95)
            if any(w in text_lower for w in ["thank", "appreciate", "grateful"]):
                emotions["gratitude"] = min(0.70 + (intensity * 0.20), 0.90)
        elif any(w in text_lower for w in ["good", "nice", "great", "happy", "enjoyed"]):
            emotions["joy"] = min(0.60 + (intensity * 0.20), 0.80)
        if any(w in text_lower for w in ["surprised", "unexpected", "wow", "amazing"]):
            emotions["surprise"] = min(0.60 + (intensity * 0.15), 0.75)
        if not emotions:
            emotions["joy"] = 0.65

    elif sentiment_label == "NEGATIVE":
        if any(w in text_lower for w in ["sick", "poisoning", "vomit", "nausea", "disgusting", "gross"]):
            emotions["disgust"] = min(0.80 + (intensity * 0.15), 0.95)
            emotions["anger"] = min(0.70 + (intensity * 0.15), 0.85)
        elif any(w in text_lower for w in ["terrible", "worst", "horrible", "awful", "hate", "never again"]):
            emotions["anger"] = min(0.75 + (intensity * 0.15), 0.90)
            emotions["disappointment"] = min(0.65 + (intensity * 0.15), 0.80)
        elif any(w in text_lower for w in ["bad", "poor", "disappointing", "disappointed", "sad"]):
            emotions["sadness"] = min(0.65 + (intensity * 0.15), 0.80)
            emotions["disappointment"] = min(0.60 + (intensity * 0.15), 0.75)
        elif any(w in text_lower for w in ["scared", "afraid", "worried", "concern"]):
            emotions["fear"] = min(0.60 + (intensity * 0.15), 0.75)
        else:
            emotions["sadness"] = 0.60
    else:
        emotions["neutral"] = 0.70

    return emotions


def extract_aspects(text: str) -> List[Dict]:
    """Extract aspects from review text using keyword matching"""
    aspects = []
    text_lower = text.lower()

    aspect_keywords = {
        "food": ["food", "meal", "dish", "taste", "flavor", "cuisine", "menu", "pasta", "pizza", "burger"],
        "service": ["service", "staff", "waiter", "server", "waitress", "employee", "manager"],
        "ambiance": ["atmosphere", "ambiance", "decor", "environment", "vibe", "setting", "music"],
        "price": ["price", "expensive", "cheap", "value", "cost", "worth", "affordable"],
        "cleanliness": ["clean", "dirty", "hygiene", "sanitary", "tidy"],
        "location": ["location", "parking", "access", "convenient", "area"],
    }

    for aspect, keywords in aspect_keywords.items():
        if any(w in text_lower for w in keywords):
            sentiment_result = analyze_sentiment(text)
            aspects.append({"aspect": aspect, "sentiment": sentiment_result["label"].lower()})

    return aspects if aspects else [{"aspect": "general", "sentiment": "positive"}]


def generate_ai_response(text: str, sentiment: str, business_name: str, aspects: Optional[List[Dict]] = None) -> str:
    """Generate a contextual AI response based on sentiment and review content"""
    business_name = business_name or "our business"
    text_lower = text.lower()

    aspect_names = {a.get("aspect", "") for a in (aspects or [])}

    if sentiment == "POSITIVE":
        parts = []
        if any(w in text_lower for w in ["love", "loved", "favorite"]):
            parts.append("We're so happy to hear you loved your experience!")
        elif any(w in text_lower for w in ["amazing", "excellent", "perfect"]):
            parts.append("Thank you for the amazing feedback!")
        elif any(w in text_lower for w in ["great", "good", "nice"]):
            parts.append("We're delighted you had a great visit!")
        else:
            parts.append("Thank you for taking the time to share your experience!")

        if "food" in aspect_names:
            parts.append("We're glad our food hit the spot!")
        if "service" in aspect_names:
            parts.append("Our team works hard to provide excellent service!")
        if "ambiance" in aspect_names:
            parts.append("We're happy you enjoyed the atmosphere!")

        if any(w in text_lower for w in ["back", "again", "return"]):
            parts.append("We can't wait to see you again!")
        else:
            parts.append(f"We hope to welcome you back to {business_name} soon!")

        return " ".join(parts)

    elif sentiment == "NEGATIVE":
        parts = []

        if any(w in text_lower for w in ["sick", "poisoning", "food poisoning", "ill"]):
            return (
                "We are deeply concerned about your health issue and sincerely apologize. "
                "This is absolutely unacceptable, and we take food safety extremely seriously. "
                "We will investigate this immediately and take all necessary steps to prevent this from happening again."
            )

        if any(w in text_lower for w in ["terrible", "worst", "horrible", "awful", "disgusting"]):
            parts.append("We sincerely apologize for this unacceptable experience.")
        elif any(w in text_lower for w in ["disappointed", "disappointing", "expected better"]):
            parts.append("We're truly sorry we didn't meet your expectations.")
        else:
            parts.append("We apologize for the issues you experienced.")

        if "food" in aspect_names:
            parts.append("We're committed to maintaining high food quality standards.")
        if "service" in aspect_names:
            if any(w in text_lower for w in ["rude", "unprofessional"]):
                parts.append("This behavior is unacceptable and we'll address it with our staff immediately.")
            elif any(w in text_lower for w in ["slow", "wait", "long"]):
                parts.append("We understand your time is valuable and will work on improving our speed.")
            else:
                parts.append("Our team will receive additional training to prevent this.")
        if "price" in aspect_names:
            parts.append("We appreciate your feedback on pricing and value.")

        parts.append(f"Please give us another chance to make things right at {business_name}.")
        return " ".join(parts)

    else:
        return (
            f"Thank you for sharing your feedback about {business_name}. "
            "We appreciate your input and are always working to improve our service!"
        )


def process_review_full(text: str, business_name: str, rating: Optional[float] = None) -> Dict:
    """Run full NLP pipeline on a single review"""
    sentiment_result = analyze_sentiment(text, rating)
    emotion_result = detect_emotions(text, sentiment_result["label"])
    aspect_result = extract_aspects(text)
    ai_response = generate_ai_response(text, sentiment_result["label"], business_name, aspect_result)

    return {
        "sentiment": sentiment_result,
        "emotions": emotion_result,
        "aspects": aspect_result,
        "ai_response": ai_response,
    }


# ==================== AUTH MODELS ====================

class UserSignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: str = Field(..., min_length=1, max_length=200)
    business_name: Optional[str] = Field(None, max_length=200)

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


# ==================== AUTH ENDPOINTS ====================

@app.post("/api/auth/signup")
async def signup(user_data: UserSignupRequest, db: Session = Depends(get_db)):
    if not DB_AVAILABLE:
        raise HTTPException(status_code=503, detail="Database not available")
    try:
        from auth import create_user, create_access_token, UserCreate
        from database import User
        existing = db.query(User).filter(User.email == user_data.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        from auth import get_password_hash
        from database import Business
        business_id = None
        if user_data.business_name:
            biz = Business(name=user_data.business_name, industry="restaurant")
            db.add(biz)
            db.commit()
            db.refresh(biz)
            business_id = biz.id
        user = User(
            email=user_data.email,
            hashed_password=get_password_hash(user_data.password),
            full_name=user_data.full_name,
            business_id=business_id,
            role="admin" if business_id else "manager"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        from auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
        token = create_access_token({"sub": user.email, "user_id": user.id})
        return {
            "access_token": token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role,
                "business_id": user.business_id,
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Signup error: %s", e)
        raise HTTPException(status_code=500, detail="Signup failed")


@app.post("/api/auth/login")
async def login(credentials: UserLoginRequest, db: Session = Depends(get_db)):
    if not DB_AVAILABLE:
        raise HTTPException(status_code=503, detail="Database not available")
    try:
        from auth import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
        user = authenticate_user(db, credentials.email, credentials.password)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        token = create_access_token({"sub": user.email, "user_id": user.id})
        return {
            "access_token": token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role,
                "business_id": user.business_id,
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Login error: %s", e)
        raise HTTPException(status_code=500, detail="Login failed")


@app.get("/api/auth/me")
async def get_me(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    if not DB_AVAILABLE:
        raise HTTPException(status_code=503, detail="Database not available")
    try:
        from auth import decode_access_token
        from database import User
        token_data = decode_access_token(credentials.credentials)
        user = db.query(User).filter(User.email == token_data.email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "business_id": user.business_id,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")


# ==================== HEALTH / ROOT ====================

@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "RevuIQ API",
        "version": "1.0.0",
        "nlp_available": NLP_AVAILABLE,
        "db_available": DB_AVAILABLE,
        "endpoints": {
            "analyze": "/api/analyze",
            "bulk_analyze": "/api/bulk-analyze",
            "generate_response": "/api/generate-response",
            "stats": "/api/stats",
            "health": "/health",
            "docs": "/docs",
        },
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "nlp_available": NLP_AVAILABLE,
        "db_available": DB_AVAILABLE,
        "version": "1.0.0",
    }


# ==================== NLP ENDPOINTS ====================

@app.post("/api/analyze")
@limiter.limit("30/minute")
async def analyze_review(request: Request, review: AnalyzeRequest):
    """
    Analyze a single review.
    Returns sentiment, emotions, aspects, and AI-generated response.
    """
    try:
        logger.info("Analyzing review, text_length=%d", len(review.text))
        result = process_review_full(
            review.text,
            review.business_name or "our business",
            review.rating,
        )
        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            **result,
        }
    except Exception as e:
        logger.error("Error analyzing review: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/bulk-analyze")
@limiter.limit("5/minute")
async def bulk_analyze(request: Request, body: BulkAnalysisRequest):
    """
    Analyze multiple reviews at once.
    Returns analysis for all reviews.
    """
    try:
        logger.info("Bulk analyzing %d reviews", len(body.reviews))
        results = []
        for review in body.reviews:
            result = process_review_full(
                review.text,
                review.business_name or "our business",
                review.rating,
            )
            results.append({"text": review.text, **result})

        return {
            "success": True,
            "count": len(results),
            "results": results,
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error("Error in bulk analysis: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate-response")
@limiter.limit("30/minute")
async def generate_response_endpoint(request: Request, body: GenerateResponseRequest):
    """
    Generate an AI response for a review.
    """
    try:
        business = body.business_name or "our business"
        sentiment = body.sentiment or analyze_sentiment(body.review_text).get("label", "NEUTRAL")
        response_text = generate_ai_response(body.review_text, sentiment, business)

        return {
            "success": True,
            "ai_response": response_text,
            "tone": body.tone,
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error("Error generating response: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats")
async def get_stats():
    """Get API statistics and model info"""
    return {
        "version": "1.0.0",
        "nlp_engine": "VADER + TextBlob" if NLP_AVAILABLE else "unavailable",
        "nlp_available": NLP_AVAILABLE,
        "db_available": DB_AVAILABLE,
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
    }


# ==================== RESTAURANT ENDPOINTS (require DB) ====================

def _require_db():
    if not DB_AVAILABLE:
        raise HTTPException(status_code=503, detail="Database not available")


@app.post("/api/restaurants")
async def create_restaurant(restaurant: RestaurantCreate, db: Session = Depends(get_db) if DB_AVAILABLE else None):
    _require_db()
    try:
        new_business = Business(
            name=restaurant.name,
            industry=restaurant.industry,
            created_at=datetime.utcnow(),
        )
        db.add(new_business)
        db.commit()
        db.refresh(new_business)
        logger.info("Created restaurant id=%d name=%s", new_business.id, new_business.name)
        return {
            "success": True,
            "restaurant": {
                "id": new_business.id,
                "name": new_business.name,
                "industry": new_business.industry,
                "created_at": new_business.created_at.isoformat(),
            },
        }
    except Exception as e:
        db.rollback()
        logger.error("Error creating restaurant: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/restaurants")
async def get_restaurants(db: Session = Depends(get_db) if DB_AVAILABLE else None):
    _require_db()
    try:
        businesses = db.query(Business).all()
        restaurants = []
        for b in businesses:
            review_count = db.query(Review).filter(Review.business_id == b.id).count()
            restaurants.append({
                "id": b.id,
                "name": b.name,
                "industry": b.industry,
                "created_at": b.created_at.isoformat() if b.created_at else None,
                "review_count": review_count,
            })
        return {"success": True, "count": len(restaurants), "restaurants": restaurants}
    except Exception as e:
        logger.error("Error listing restaurants: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/restaurants/{restaurant_id}")
async def get_restaurant(restaurant_id: int, db: Session = Depends(get_db) if DB_AVAILABLE else None):
    _require_db()
    try:
        business = db.query(Business).filter(Business.id == restaurant_id).first()
        if not business:
            raise HTTPException(status_code=404, detail="Restaurant not found")

        reviews = db.query(Review).filter(Review.business_id == restaurant_id).all()
        sentiment_counts = {"POSITIVE": 0, "NEUTRAL": 0, "NEGATIVE": 0}
        ratings = []

        for r in reviews:
            if r.sentiment:
                key = r.sentiment.upper()
                sentiment_counts[key] = sentiment_counts.get(key, 0) + 1
            if r.rating:
                ratings.append(r.rating)

        avg_rating = sum(ratings) / len(ratings) if ratings else 0

        return {
            "success": True,
            "restaurant": {
                "id": business.id,
                "name": business.name,
                "industry": business.industry,
                "created_at": business.created_at.isoformat() if business.created_at else None,
                "stats": {
                    "total_reviews": len(reviews),
                    "average_rating": round(avg_rating, 2),
                    "sentiment_distribution": sentiment_counts,
                },
            },
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error getting restaurant %d: %s", restaurant_id, e)
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/restaurants/{restaurant_id}")
async def delete_restaurant(restaurant_id: int, db: Session = Depends(get_db) if DB_AVAILABLE else None):
    _require_db()
    try:
        business = db.query(Business).filter(Business.id == restaurant_id).first()
        if not business:
            raise HTTPException(status_code=404, detail="Restaurant not found")

        name = business.name
        db.query(Review).filter(Review.business_id == restaurant_id).delete()
        db.delete(business)
        db.commit()
        logger.info("Deleted restaurant id=%d name=%s", restaurant_id, name)
        return {"success": True, "message": f"Restaurant '{name}' and all its reviews deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error("Error deleting restaurant %d: %s", restaurant_id, e)
        raise HTTPException(status_code=500, detail=str(e))


# ==================== REVIEW ENDPOINTS ====================

@app.post("/api/reviews")
async def create_review(review: ReviewCreate, db: Session = Depends(get_db) if DB_AVAILABLE else None):
    _require_db()
    try:
        existing = db.query(Review).filter(Review.platform_review_id == review.platform_review_id).first()
        if existing:
            return {"success": False, "message": "Review already exists", "review_id": existing.id}

        analysis = process_review_full(review.text, "our business", review.rating)

        new_review = Review(
            platform=review.platform,
            platform_review_id=review.platform_review_id,
            business_id=review.business_id,
            author_name=review.author_name,
            rating=review.rating,
            text=review.text,
            review_date=review.review_date,
            sentiment=analysis["sentiment"]["label"].lower(),
            sentiment_score=analysis["sentiment"]["score"],
            emotions=json.dumps(analysis["emotions"]),
            aspects=json.dumps(analysis["aspects"]),
            ai_response=analysis["ai_response"],
            created_at=datetime.utcnow(),
        )

        db.add(new_review)
        db.commit()
        db.refresh(new_review)
        logger.info("Created review id=%d platform=%s", new_review.id, review.platform)

        return {"success": True, "review_id": new_review.id, "analysis": analysis}
    except Exception as e:
        db.rollback()
        logger.error("Error creating review: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/reviews/bulk")
async def create_bulk_reviews(bulk: ReviewBulkCreate, db: Session = Depends(get_db) if DB_AVAILABLE else None):
    _require_db()
    try:
        created_count = 0
        skipped_count = 0

        for review_data in bulk.reviews:
            pid = review_data.get("platform_review_id", f"manual_{datetime.now().timestamp()}_{created_count}")
            existing = db.query(Review).filter(Review.platform_review_id == pid).first()
            if existing:
                skipped_count += 1
                continue

            text = review_data.get("text", "")
            rating = review_data.get("rating", 5)

            analysis = process_review_full(text, review_data.get("business_name", "our business"), rating)

            new_review = Review(
                platform=review_data.get("platform", "manual"),
                platform_review_id=pid,
                business_id=bulk.business_id,
                author_name=review_data.get("author_name", review_data.get("author", "Anonymous")),
                rating=rating,
                text=text,
                review_date=datetime.fromisoformat(review_data["review_date"])
                if review_data.get("review_date")
                else datetime.utcnow(),
                sentiment=analysis["sentiment"]["label"].lower(),
                sentiment_score=analysis["sentiment"]["score"],
                emotions=json.dumps(analysis["emotions"]),
                aspects=json.dumps(analysis["aspects"]),
                ai_response=analysis["ai_response"],
                approval_status="approved",
                is_genuine=True,
                approved_at=datetime.utcnow(),
                created_at=datetime.utcnow(),
            )
            db.add(new_review)
            created_count += 1

        db.commit()
        logger.info("Bulk created %d reviews, skipped %d", created_count, skipped_count)
        return {"success": True, "created": created_count, "skipped": skipped_count, "total": len(bulk.reviews)}
    except Exception as e:
        db.rollback()
        logger.error("Error bulk creating reviews: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/reviews/restaurant/{restaurant_id}")
async def get_restaurant_reviews(
    restaurant_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db) if DB_AVAILABLE else None,
):
    _require_db()
    try:
        reviews = (
            db.query(Review)
            .filter(Review.business_id == restaurant_id, Review.approval_status == "approved")
            .order_by(Review.review_date.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

        return {
            "success": True,
            "count": len(reviews),
            "reviews": [
                {
                    "id": r.id,
                    "platform": r.platform,
                    "author": r.author_name,
                    "rating": r.rating,
                    "text": r.text,
                    "date": r.review_date.isoformat() if r.review_date else None,
                    "sentiment": r.sentiment,
                    "sentiment_score": r.sentiment_score,
                    "emotions": json.loads(r.emotions) if r.emotions else {},
                    "aspects": json.loads(r.aspects) if r.aspects else [],
                    "ai_response": r.ai_response,
                }
                for r in reviews
            ],
        }
    except Exception as e:
        logger.error("Error getting reviews for restaurant %d: %s", restaurant_id, e)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/reviews/pending")
async def get_pending_reviews(db: Session = Depends(get_db) if DB_AVAILABLE else None):
    _require_db()
    try:
        reviews = (
            db.query(Review)
            .filter(Review.approval_status == "pending")
            .order_by(Review.created_at.desc())
            .limit(50)
            .all()
        )

        return {
            "success": True,
            "count": len(reviews),
            "reviews": [
                {
                    "id": r.id,
                    "business_id": r.business_id,
                    "author": r.author_name,
                    "rating": r.rating,
                    "text": r.text,
                    "review_date": r.review_date.isoformat() if r.review_date else None,
                    "sentiment": r.sentiment,
                    "sentiment_score": r.sentiment_score,
                    "ai_response": r.ai_response,
                    "created_at": r.created_at.isoformat() if r.created_at else None,
                    "approval_status": r.approval_status,
                }
                for r in reviews
            ],
        }
    except Exception as e:
        logger.error("Error getting pending reviews: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/reviews/stats")
async def get_review_stats(db: Session = Depends(get_db) if DB_AVAILABLE else None):
    _require_db()
    try:
        total = db.query(Review).count()
        pending = db.query(Review).filter(Review.approval_status == "pending").count()
        approved = db.query(Review).filter(Review.approval_status == "approved").count()
        rejected = db.query(Review).filter(Review.approval_status == "rejected").count()

        return {"success": True, "stats": {"total": total, "pending": pending, "approved": approved, "rejected": rejected}}
    except Exception as e:
        logger.error("Error getting review stats: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/reviews/{review_id}/approve")
async def approve_review(
    review_id: int,
    approval: ApprovalRequest,
    db: Session = Depends(get_db) if DB_AVAILABLE else None,
):
    _require_db()
    try:
        review = db.query(Review).filter(Review.id == review_id).first()
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")

        review.approval_status = "approved" if approval.is_genuine else "rejected"
        review.is_genuine = approval.is_genuine
        review.approval_notes = approval.notes
        review.approved_at = datetime.utcnow()
        db.commit()

        logger.info("Review %d set to %s", review_id, review.approval_status)
        return {
            "success": True,
            "message": f"Review {'approved' if approval.is_genuine else 'rejected'} successfully",
            "review_id": review_id,
            "status": review.approval_status,
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error("Error approving review %d: %s", review_id, e)
        raise HTTPException(status_code=500, detail=str(e))


# ==================== RESPONSE APPROVAL ENDPOINTS ====================

@app.get("/api/responses/pending")
async def get_pending_responses(db: Session = Depends(get_db) if DB_AVAILABLE else None):
    _require_db()
    try:
        reviews = (
            db.query(Review)
            .filter(Review.ai_response.isnot(None), Review.human_approved == False)
            .order_by(Review.created_at.desc())
            .limit(20)
            .all()
        )

        return {
            "success": True,
            "count": len(reviews),
            "reviews": [
                {
                    "id": r.id,
                    "business_id": r.business_id,
                    "author": r.author_name,
                    "rating": r.rating,
                    "text": r.text,
                    "review_date": r.review_date.isoformat() if r.review_date else None,
                    "sentiment": r.sentiment,
                    "ai_response": r.ai_response,
                    "response_tone": r.response_tone,
                    "human_approved": r.human_approved,
                    "final_response": r.final_response,
                    "response_posted": r.response_posted,
                    "created_at": r.created_at.isoformat() if r.created_at else None,
                }
                for r in reviews
            ],
        }
    except Exception as e:
        logger.error("Error getting pending responses: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/responses/stats")
async def get_response_stats(db: Session = Depends(get_db) if DB_AVAILABLE else None):
    _require_db()
    try:
        total_with_ai = db.query(Review).filter(Review.ai_response.isnot(None)).count()
        pending = db.query(Review).filter(Review.ai_response.isnot(None), Review.human_approved == False).count()
        approved = db.query(Review).filter(Review.human_approved == True).count()
        posted = db.query(Review).filter(Review.response_posted == True).count()

        return {
            "success": True,
            "stats": {
                "total_with_ai_response": total_with_ai,
                "pending_approval": pending,
                "approved": approved,
                "posted": posted,
            },
        }
    except Exception as e:
        logger.error("Error getting response stats: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/responses/{review_id}/approve")
async def approve_response(
    review_id: int,
    approval: ResponseApprovalRequest,
    db: Session = Depends(get_db) if DB_AVAILABLE else None,
):
    _require_db()
    try:
        review = db.query(Review).filter(Review.id == review_id).first()
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")

        if approval.approved:
            review.final_response = approval.edited_response or review.ai_response
            review.human_approved = True
            message = "Response approved and ready to post"
        else:
            review.final_response = None
            review.human_approved = False
            message = "Response rejected"

        review.updated_at = datetime.utcnow()
        db.commit()

        logger.info("Response for review %d: approved=%s", review_id, approval.approved)
        return {"success": True, "message": message, "review_id": review_id, "approved": approval.approved}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error("Error approving response for review %d: %s", review_id, e)
        raise HTTPException(status_code=500, detail=str(e))


# ==================== GOOGLE PLACES INTEGRATION ====================

@app.post("/api/google/fetch-reviews")
async def fetch_google_reviews_endpoint(
    req: GooglePlacesRequest,
    db: Session = Depends(get_db) if DB_AVAILABLE else None,
):
    _require_db()
    if not GOOGLE_AVAILABLE:
        raise HTTPException(status_code=503, detail="Google Places integration not available")

    google_api_key = os.getenv("GOOGLE_PLACES_API_KEY", "")
    if not google_api_key:
        raise HTTPException(
            status_code=400,
            detail="Google Places API key not configured. Please add GOOGLE_PLACES_API_KEY to your .env file",
        )

    try:
        google_reviews = fetch_google_reviews(req.restaurant_name, req.location, google_api_key)

        if not google_reviews:
            return {"success": False, "created": 0, "skipped": 0, "total": 0,
                    "message": "No reviews found or API quota exceeded"}

        created_count = 0
        skipped_count = 0

        for review_data in google_reviews:
            existing = db.query(Review).filter(
                Review.platform == "google",
                Review.platform_review_id == review_data.get("platform_review_id", ""),
                Review.business_id == req.business_id,
            ).first()

            if existing:
                skipped_count += 1
                continue

            text = review_data.get("text", "")
            rating = review_data.get("rating", 5)
            analysis = process_review_full(text, req.restaurant_name, rating)

            new_review = Review(
                platform="google",
                platform_review_id=review_data.get("platform_review_id", f"google_{datetime.now().timestamp()}"),
                business_id=req.business_id,
                author_name=review_data.get("author_name", "Anonymous"),
                rating=rating,
                text=text,
                review_date=datetime.fromtimestamp(review_data.get("time", datetime.now().timestamp())),
                sentiment=analysis["sentiment"]["label"].lower(),
                sentiment_score=analysis["sentiment"]["score"],
                emotions=json.dumps(analysis["emotions"]),
                aspects=json.dumps(analysis["aspects"]),
                ai_response=analysis["ai_response"],
                approval_status="approved",
                is_genuine=True,
                approved_at=datetime.utcnow(),
                created_at=datetime.utcnow(),
            )
            db.add(new_review)
            created_count += 1

        db.commit()
        logger.info("Fetched Google reviews: created=%d skipped=%d", created_count, skipped_count)
        return {
            "success": True,
            "created": created_count,
            "skipped": skipped_count,
            "total": len(google_reviews),
            "message": f"Fetched {created_count} reviews from Google Places",
        }
    except Exception as e:
        if DB_AVAILABLE and db:
            db.rollback()
        logger.error("Error fetching Google reviews: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/google/restaurant-info")
async def get_google_restaurant_info(restaurant_name: str, location: str = ""):
    if not GOOGLE_AVAILABLE:
        raise HTTPException(status_code=503, detail="Google Places integration not available")
    try:
        info = get_restaurant_details(restaurant_name, location)
        if info:
            return {"success": True, "restaurant": info}
        return {"success": False, "message": "Restaurant not found or API key not configured"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== ANALYTICS ENDPOINTS ====================

@app.get("/api/analytics/stats")
async def get_analytics_stats(db: Session = Depends(get_db) if DB_AVAILABLE else None):
    _require_db()
    try:
        total_reviews = db.query(Review).filter(Review.approval_status == "approved").count()
        total_businesses = db.query(Business).count()
        pending_reviews = db.query(Review).filter(Review.approval_status == "pending").count()

        positive = db.query(Review).filter(
            Review.approval_status == "approved",
            Review.sentiment.in_(["positive", "POSITIVE"]),
        ).count()
        negative = db.query(Review).filter(
            Review.approval_status == "approved",
            Review.sentiment.in_(["negative", "NEGATIVE"]),
        ).count()

        avg_rating = db.query(func.avg(Review.rating)).filter(Review.approval_status == "approved").scalar() or 0

        reviews_with_responses = db.query(Review).filter(
            Review.approval_status == "approved",
            Review.ai_response.isnot(None),
            Review.ai_response != "",
        ).count()
        response_rate = round((reviews_with_responses / total_reviews * 100), 1) if total_reviews > 0 else 0

        return {
            "success": True,
            "total_reviews": total_reviews,
            "total_businesses": total_businesses,
            "pending_reviews": pending_reviews,
            "avg_rating": round(float(avg_rating), 2),
            "positive_reviews": positive,
            "negative_reviews": negative,
            "response_rate": response_rate,
            "response_stats": {
                "total_reviews": total_reviews,
                "approved_responses": reviews_with_responses,
                "posted_responses": 0,
                "pending_reviews": pending_reviews,
                "approval_rate": response_rate,
                "post_rate": 0,
            },
            "average_rating": round(float(avg_rating), 2),
        }
    except Exception as e:
        logger.error("Error getting analytics stats: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/analytics/sentiment-distribution")
async def get_sentiment_distribution(
    days: int = 30,
    business_id: Optional[int] = None,
    db: Session = Depends(get_db) if DB_AVAILABLE else None,
):
    _require_db()
    try:
        since_date = datetime.utcnow() - timedelta(days=days)
        query = db.query(Review).filter(
            Review.review_date >= since_date,
            Review.approval_status == "approved",
        )
        if business_id:
            query = query.filter(Review.business_id == business_id)

        reviews = query.all()

        distribution = {"POSITIVE": 0, "NEUTRAL": 0, "NEGATIVE": 0}
        for r in reviews:
            if r.sentiment:
                key = r.sentiment.upper()
                distribution[key] = distribution.get(key, 0) + 1

        return {"success": True, "distribution": distribution, "total": len(reviews), "period_days": days}
    except Exception as e:
        logger.error("Error getting sentiment distribution: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/analytics/emotion-distribution")
async def get_emotion_distribution(
    days: int = 30,
    business_id: Optional[int] = None,
    db: Session = Depends(get_db) if DB_AVAILABLE else None,
):
    _require_db()
    try:
        since_date = datetime.utcnow() - timedelta(days=days)
        query = db.query(Review).filter(
            Review.review_date >= since_date,
            Review.approval_status == "approved",
        )
        if business_id:
            query = query.filter(Review.business_id == business_id)

        reviews = query.all()

        emotion_counts: Dict[str, int] = {}
        for r in reviews:
            if r.emotions:
                try:
                    emotions = json.loads(r.emotions)
                    if emotions:
                        primary = max(emotions.items(), key=lambda x: x[1])
                        emotion_counts[primary[0]] = emotion_counts.get(primary[0], 0) + 1
                except Exception:
                    pass

        return {"success": True, "distribution": emotion_counts, "total": len(reviews), "period_days": days}
    except Exception as e:
        logger.error("Error getting emotion distribution: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/analytics/restaurant/{restaurant_id}")
async def get_restaurant_analytics(
    restaurant_id: int,
    days: int = 365,
    db: Session = Depends(get_db) if DB_AVAILABLE else None,
):
    _require_db()
    try:
        reviews = (
            db.query(Review)
            .filter(Review.business_id == restaurant_id, Review.approval_status == "approved")
            .all()
        )

        if not reviews:
            return {
                "success": True,
                "total_reviews": 0,
                "average_rating": 0,
                "sentiment_distribution": {"POSITIVE": 0, "NEUTRAL": 0, "NEGATIVE": 0},
                "top_emotions": {},
                "top_aspects": {},
                "rating_distribution": {"5_star": 0, "4_star": 0, "3_star": 0, "2_star": 0, "1_star": 0},
            }

        total_reviews = len(reviews)
        ratings = [r.rating for r in reviews if r.rating]
        avg_rating = sum(ratings) / len(ratings) if ratings else 0

        positive = sum(1 for r in reviews if r.sentiment and r.sentiment.lower() == "positive")
        negative = sum(1 for r in reviews if r.sentiment and r.sentiment.lower() == "negative")
        neutral = sum(1 for r in reviews if r.sentiment and r.sentiment.lower() == "neutral")

        emotions: Dict[str, float] = {}
        aspects: Dict[str, int] = {}

        for r in reviews:
            if r.emotions:
                try:
                    emotion_data = json.loads(r.emotions)
                    for emotion, score in emotion_data.items():
                        emotions[emotion] = emotions.get(emotion, 0) + score
                except Exception:
                    pass

            if r.aspects:
                try:
                    aspect_data = json.loads(r.aspects)
                    for aspect in aspect_data:
                        name = aspect if isinstance(aspect, str) else aspect.get("aspect", "unknown")
                        aspects[name] = aspects.get(name, 0) + 1
                except Exception:
                    pass

        return {
            "success": True,
            "total_reviews": total_reviews,
            "average_rating": round(avg_rating, 2),
            "sentiment_distribution": {"POSITIVE": positive, "NEUTRAL": neutral, "NEGATIVE": negative},
            "top_emotions": dict(sorted(emotions.items(), key=lambda x: x[1], reverse=True)[:5]),
            "top_aspects": dict(sorted(aspects.items(), key=lambda x: x[1], reverse=True)[:5]),
            "rating_distribution": {
                "5_star": sum(1 for r in ratings if r == 5),
                "4_star": sum(1 for r in ratings if r == 4),
                "3_star": sum(1 for r in ratings if r == 3),
                "2_star": sum(1 for r in ratings if r == 2),
                "1_star": sum(1 for r in ratings if r == 1),
            },
        }
    except Exception as e:
        logger.error("Error getting restaurant analytics for %d: %s", restaurant_id, e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/reviews/reanalyze-all")
async def reanalyze_all_reviews(db: Session = Depends(get_db) if DB_AVAILABLE else None):
    """Re-analyze all reviews with the current NLP pipeline"""
    _require_db()
    try:
        reviews = db.query(Review).all()
        updated_count = 0

        for review in reviews:
            if review.text:
                analysis = process_review_full(review.text, "our business", review.rating)
                review.sentiment = analysis["sentiment"]["label"].lower()
                review.sentiment_score = analysis["sentiment"]["score"]
                review.emotions = json.dumps(analysis["emotions"])
                review.aspects = json.dumps(analysis["aspects"])
                review.ai_response = analysis["ai_response"]
                updated_count += 1

        db.commit()
        logger.info("Reanalyzed %d reviews", updated_count)
        return {"success": True, "updated": updated_count, "message": f"Re-analyzed {updated_count} reviews"}
    except Exception as e:
        db.rollback()
        logger.error("Error reanalyzing reviews: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


# ==================== RUN SERVER ====================

if __name__ == "__main__":
    logger.info("Starting RevuIQ API Server")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
