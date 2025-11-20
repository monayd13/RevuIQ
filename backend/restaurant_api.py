"""
Restaurant Review API with NLP Analytics
Complete endpoints for restaurant review management and analytics
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
import json
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db, Review, Business, Analytics, init_db
from nlp_pipeline.sentiment_analyzer import SentimentAnalyzer
from nlp_pipeline.emotion_detector import EmotionDetector
from nlp_pipeline.aspect_extractor import AspectExtractor
from nlp_pipeline.response_generator import ResponseGenerator

# Initialize FastAPI
app = FastAPI(
    title="RevuIQ Restaurant API",
    description="Restaurant Review Management with NLP Analytics",
    version="2.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# NLP Models (lazy loading)
sentiment_analyzer = None
emotion_detector = None
aspect_extractor = None
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

def get_aspect_extractor():
    global aspect_extractor
    if aspect_extractor is None:
        aspect_extractor = AspectExtractor()
    return aspect_extractor

def get_response_generator():
    global response_generator
    if response_generator is None:
        response_generator = ResponseGenerator()
    return response_generator


# ==================== DATA MODELS ====================

class RestaurantCreate(BaseModel):
    name: str
    industry: str = "restaurant"

class ReviewCreate(BaseModel):
    platform: str
    platform_review_id: str
    business_id: int
    author_name: str
    rating: float
    text: str
    review_date: datetime

class ReviewBulkCreate(BaseModel):
    business_id: int
    reviews: List[Dict]

class AnalyticsQuery(BaseModel):
    business_id: Optional[int] = None
    days: int = 30


# ==================== HEALTH CHECK ====================

@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "RevuIQ Restaurant API",
        "version": "2.0.0",
        "endpoints": {
            "restaurants": "/api/restaurants",
            "reviews": "/api/reviews",
            "analytics": "/api/analytics"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "models_loaded": {
            "sentiment": sentiment_analyzer is not None,
            "emotion": emotion_detector is not None,
            "aspect": aspect_extractor is not None,
            "response": response_generator is not None
        }
    }


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
        return {
            "success": True,
            "count": len(businesses),
            "restaurants": [
                {
                    "id": b.id,
                    "name": b.name,
                    "industry": b.industry,
                    "created_at": b.created_at.isoformat(),
                    "review_count": len(b.reviews)
                }
                for b in businesses
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/restaurants/{restaurant_id}")
async def get_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    """Get restaurant details with summary analytics"""
    try:
        business = db.query(Business).filter(Business.id == restaurant_id).first()
        if not business:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        
        # Get review stats
        reviews = db.query(Review).filter(Review.business_id == restaurant_id).all()
        
        sentiment_counts = {"POSITIVE": 0, "NEUTRAL": 0, "NEGATIVE": 0}
        total_rating = 0
        
        for review in reviews:
            if review.sentiment:
                sentiment_counts[review.sentiment] = sentiment_counts.get(review.sentiment, 0) + 1
            if review.rating:
                total_rating += review.rating
        
        avg_rating = total_rating / len(reviews) if reviews else 0
        
        return {
            "success": True,
            "restaurant": {
                "id": business.id,
                "name": business.name,
                "industry": business.industry,
                "created_at": business.created_at.isoformat(),
                "stats": {
                    "total_reviews": len(reviews),
                    "average_rating": round(avg_rating, 2),
                    "sentiment_distribution": sentiment_counts
                }
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== REVIEW ENDPOINTS ====================

@app.post("/api/reviews")
async def create_review_with_analysis(review: ReviewCreate, db: Session = Depends(get_db)):
    """Create a review and run NLP analysis"""
    try:
        # Check if review already exists
        existing = db.query(Review).filter(
            Review.platform_review_id == review.platform_review_id
        ).first()
        
        if existing:
            return {
                "success": False,
                "message": "Review already exists",
                "review_id": existing.id
            }
        
        # Create review
        new_review = Review(
            platform=review.platform,
            platform_review_id=review.platform_review_id,
            business_id=review.business_id,
            author_name=review.author_name,
            rating=review.rating,
            text=review.text,
            review_date=review.review_date,
            created_at=datetime.utcnow()
        )
        
        # Run NLP analysis
        sentiment_result = get_sentiment_analyzer().analyze(review.text)
        emotion_result = get_emotion_detector().detect(review.text)
        aspect_result = get_aspect_extractor().extract(review.text)
        
        # Store analysis results
        new_review.sentiment = sentiment_result.get('label')
        new_review.sentiment_score = sentiment_result.get('score')
        new_review.emotions = json.dumps(emotion_result)
        new_review.aspects = json.dumps(aspect_result)
        
        # Generate AI response
        ai_response = get_response_generator().generate(
            review_text=review.text,
            sentiment=sentiment_result.get('label'),
            tone="professional"
        )
        new_review.ai_response = ai_response
        
        db.add(new_review)
        db.commit()
        db.refresh(new_review)
        
        return {
            "success": True,
            "review_id": new_review.id,
            "analysis": {
                "sentiment": sentiment_result,
                "emotions": emotion_result,
                "aspects": aspect_result,
                "ai_response": ai_response
            }
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/reviews/bulk")
async def create_bulk_reviews(bulk: ReviewBulkCreate, db: Session = Depends(get_db)):
    """Create multiple reviews with NLP analysis"""
    try:
        created_count = 0
        skipped_count = 0
        
        for review_data in bulk.reviews:
            # Check if exists
            existing = db.query(Review).filter(
                Review.platform_review_id == review_data.get('platform_review_id', '')
            ).first()
            
            if existing:
                skipped_count += 1
                continue
            
            # Create review
            new_review = Review(
                platform=review_data.get('platform', 'manual'),
                platform_review_id=review_data.get('platform_review_id', f"manual_{datetime.now().timestamp()}"),
                business_id=bulk.business_id,
                author_name=review_data.get('author_name', 'Anonymous'),
                rating=review_data.get('rating', 0),
                text=review_data.get('text', ''),
                review_date=datetime.fromisoformat(review_data.get('review_date')) if review_data.get('review_date') else datetime.utcnow(),
                created_at=datetime.utcnow()
            )
            
            # Run NLP
            if new_review.text:
                sentiment_result = get_sentiment_analyzer().analyze(new_review.text)
                emotion_result = get_emotion_detector().detect(new_review.text)
                aspect_result = get_aspect_extractor().extract(new_review.text)
                
                new_review.sentiment = sentiment_result.get('label')
                new_review.sentiment_score = sentiment_result.get('score')
                new_review.emotions = json.dumps(emotion_result)
                new_review.aspects = json.dumps(aspect_result)
                
                ai_response = get_response_generator().generate(
                    review_text=new_review.text,
                    sentiment=sentiment_result.get('label')
                )
                new_review.ai_response = ai_response
            
            db.add(new_review)
            created_count += 1
        
        db.commit()
        
        return {
            "success": True,
            "created": created_count,
            "skipped": skipped_count,
            "total": len(bulk.reviews)
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/reviews/restaurant/{restaurant_id}")
async def get_restaurant_reviews(
    restaurant_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get all reviews for a restaurant with NLP analysis"""
    try:
        reviews = db.query(Review).filter(
            Review.business_id == restaurant_id
        ).order_by(Review.review_date.desc()).offset(skip).limit(limit).all()
        
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
                    "ai_response": r.ai_response
                }
                for r in reviews
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== ANALYTICS ENDPOINTS ====================

@app.get("/api/analytics/restaurant/{restaurant_id}")
async def get_restaurant_analytics(
    restaurant_id: int,
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Get comprehensive analytics for a restaurant"""
    try:
        # Date filter
        since_date = datetime.utcnow() - timedelta(days=days)
        
        # Get reviews
        reviews = db.query(Review).filter(
            Review.business_id == restaurant_id,
            Review.review_date >= since_date
        ).all()
        
        if not reviews:
            return {
                "success": True,
                "restaurant_id": restaurant_id,
                "period_days": days,
                "message": "No reviews found for this period"
            }
        
        # Sentiment distribution
        sentiment_dist = {"POSITIVE": 0, "NEUTRAL": 0, "NEGATIVE": 0}
        
        # Emotion aggregation
        emotion_dist = {}
        
        # Aspect aggregation
        aspect_dist = {}
        
        # Rating stats
        ratings = []
        
        for review in reviews:
            # Sentiment
            if review.sentiment:
                sentiment_dist[review.sentiment] = sentiment_dist.get(review.sentiment, 0) + 1
            
            # Emotions
            if review.emotions:
                try:
                    emotions = json.loads(review.emotions)
                    for emotion, score in emotions.items():
                        if emotion not in emotion_dist:
                            emotion_dist[emotion] = []
                        emotion_dist[emotion].append(score)
                except:
                    pass
            
            # Aspects
            if review.aspects:
                try:
                    aspects = json.loads(review.aspects)
                    for aspect in aspects:
                        aspect_name = aspect.get('aspect', 'unknown')
                        aspect_dist[aspect_name] = aspect_dist.get(aspect_name, 0) + 1
                except:
                    pass
            
            # Ratings
            if review.rating:
                ratings.append(review.rating)
        
        # Calculate averages
        avg_rating = sum(ratings) / len(ratings) if ratings else 0
        
        # Top emotions (by average score)
        top_emotions = {
            emotion: round(sum(scores) / len(scores), 3)
            for emotion, scores in emotion_dist.items()
        }
        top_emotions = dict(sorted(top_emotions.items(), key=lambda x: x[1], reverse=True)[:5])
        
        # Top aspects
        top_aspects = dict(sorted(aspect_dist.items(), key=lambda x: x[1], reverse=True)[:10])
        
        return {
            "success": True,
            "restaurant_id": restaurant_id,
            "period_days": days,
            "total_reviews": len(reviews),
            "average_rating": round(avg_rating, 2),
            "sentiment_distribution": sentiment_dist,
            "top_emotions": top_emotions,
            "top_aspects": top_aspects,
            "rating_distribution": {
                "5_star": len([r for r in ratings if r >= 4.5]),
                "4_star": len([r for r in ratings if 3.5 <= r < 4.5]),
                "3_star": len([r for r in ratings if 2.5 <= r < 3.5]),
                "2_star": len([r for r in ratings if 1.5 <= r < 2.5]),
                "1_star": len([r for r in ratings if r < 1.5])
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/sentiment-distribution")
async def get_sentiment_distribution(
    days: int = 30,
    business_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get sentiment distribution across all or specific restaurant"""
    try:
        since_date = datetime.utcnow() - timedelta(days=days)
        
        query = db.query(Review).filter(Review.review_date >= since_date)
        if business_id:
            query = query.filter(Review.business_id == business_id)
        
        reviews = query.all()
        
        distribution = {"POSITIVE": 0, "NEUTRAL": 0, "NEGATIVE": 0}
        for review in reviews:
            if review.sentiment:
                distribution[review.sentiment] = distribution.get(review.sentiment, 0) + 1
        
        return {
            "success": True,
            "distribution": distribution,
            "total": len(reviews),
            "period_days": days
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/emotion-distribution")
async def get_emotion_distribution(
    days: int = 30,
    business_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get emotion distribution"""
    try:
        since_date = datetime.utcnow() - timedelta(days=days)
        
        query = db.query(Review).filter(Review.review_date >= since_date)
        if business_id:
            query = query.filter(Review.business_id == business_id)
        
        reviews = query.all()
        
        emotion_counts = {}
        for review in reviews:
            if review.emotions:
                try:
                    emotions = json.loads(review.emotions)
                    # Get primary emotion (highest score)
                    if emotions:
                        primary = max(emotions.items(), key=lambda x: x[1])
                        emotion_counts[primary[0]] = emotion_counts.get(primary[0], 0) + 1
                except:
                    pass
        
        return {
            "success": True,
            "distribution": emotion_counts,
            "total": len(reviews),
            "period_days": days
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/stats")
async def get_overall_stats(db: Session = Depends(get_db)):
    """Get overall system statistics"""
    try:
        total_reviews = db.query(Review).count()
        total_businesses = db.query(Business).count()
        
        # Reviews with responses
        reviews_with_ai = db.query(Review).filter(Review.ai_response.isnot(None)).count()
        
        # Average rating
        avg_rating_result = db.query(func.avg(Review.rating)).scalar()
        avg_rating = float(avg_rating_result) if avg_rating_result else 0
        
        return {
            "success": True,
            "total_reviews": total_reviews,
            "total_restaurants": total_businesses,
            "response_stats": {
                "total_reviews": total_reviews,
                "approved_responses": reviews_with_ai,
                "posted_responses": 0,  # TODO: Track posted responses
                "approval_rate": (reviews_with_ai / total_reviews * 100) if total_reviews > 0 else 0,
                "post_rate": 0
            },
            "average_rating": round(avg_rating, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== RUN SERVER ====================

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Initializing RevuIQ Restaurant API...")
    print("📊 Setting up database...")
    init_db()
    print("✓ Database ready!")
    
    print("\n🔥 Starting server on http://localhost:8000")
    print("📖 API docs: http://localhost:8000/docs")
    
    uvicorn.run(
        "restaurant_api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
