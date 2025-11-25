"""
Simplified Restaurant API without NLP models (for testing)
Use this if you have PyTorch compatibility issues
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
import json

from database import get_db, Review, Business, init_db
from google_places_integration import fetch_google_reviews, get_restaurant_details

# Initialize FastAPI
app = FastAPI(
    title="RevuIQ Restaurant API (Simple)",
    description="Restaurant Review Management - No NLP",
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

# ==================== MOCK NLP (Simple sentiment based on rating) ====================

def mock_sentiment_analysis(text: str, rating: float):
    """Simple sentiment based on rating"""
    if rating >= 4:
        return {"label": "POSITIVE", "score": 0.9}
    elif rating >= 3:
        return {"label": "NEUTRAL", "score": 0.8}
    else:
        return {"label": "NEGATIVE", "score": 0.85}

def mock_emotion_detection(text: str, rating: float):
    """Simple emotion based on rating"""
    if rating >= 4:
        return {"joy": 0.8, "gratitude": 0.6}
    elif rating >= 3:
        return {"neutral": 0.7}
    else:
        return {"disappointment": 0.7, "anger": 0.5}

def mock_aspect_extraction(text: str):
    """Simple aspect extraction based on keywords"""
    aspects = []
    text_lower = text.lower()
    
    if any(word in text_lower for word in ["food", "meal", "dish", "pasta", "pizza"]):
        aspects.append({"aspect": "food", "sentiment": "positive"})
    if any(word in text_lower for word in ["service", "staff", "waiter", "server"]):
        aspects.append({"aspect": "service", "sentiment": "positive"})
    if any(word in text_lower for word in ["atmosphere", "ambiance", "decor"]):
        aspects.append({"aspect": "ambiance", "sentiment": "positive"})
    if any(word in text_lower for word in ["price", "expensive", "cheap", "value"]):
        aspects.append({"aspect": "price", "sentiment": "neutral"})
    
    return aspects if aspects else [{"aspect": "general", "sentiment": "positive"}]

def mock_response_generator(text: str, sentiment: str):
    """Simple response generation"""
    if sentiment == "POSITIVE":
        return "Thank you so much for your wonderful feedback! We're thrilled to hear you had a great experience. We look forward to welcoming you back soon!"
    elif sentiment == "NEGATIVE":
        return "We sincerely apologize for your experience. Your feedback is important to us and we're working to improve. Please contact us directly so we can make this right."
    else:
        return "Thank you for your feedback! We appreciate you taking the time to share your thoughts with us."

# ==================== HEALTH CHECK ====================

@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "RevuIQ Restaurant API (Simple Mode)",
        "version": "2.0.0",
        "note": "Using mock NLP - no ML models loaded"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "mode": "simple",
        "models_loaded": False
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
    """Get restaurant details"""
    try:
        business = db.query(Business).filter(Business.id == restaurant_id).first()
        if not business:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        
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

@app.delete("/api/restaurants/{restaurant_id}")
async def delete_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    """Delete a restaurant and all its reviews"""
    try:
        business = db.query(Business).filter(Business.id == restaurant_id).first()
        if not business:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        
        # Delete all reviews for this restaurant first
        db.query(Review).filter(Review.business_id == restaurant_id).delete()
        
        # Delete the restaurant
        db.delete(business)
        db.commit()
        
        return {
            "success": True,
            "message": f"Restaurant '{business.name}' and all its reviews deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# ==================== REVIEW ENDPOINTS ====================

@app.post("/api/reviews")
async def create_review_with_analysis(review: ReviewCreate, db: Session = Depends(get_db)):
    """Create a review with mock NLP analysis"""
    try:
        existing = db.query(Review).filter(
            Review.platform_review_id == review.platform_review_id
        ).first()
        
        if existing:
            return {
                "success": False,
                "message": "Review already exists",
                "review_id": existing.id
            }
        
        # Mock NLP analysis
        sentiment_result = mock_sentiment_analysis(review.text, review.rating)
        emotion_result = mock_emotion_detection(review.text, review.rating)
        aspect_result = mock_aspect_extraction(review.text)
        ai_response = mock_response_generator(review.text, sentiment_result['label'])
        
        new_review = Review(
            platform=review.platform,
            platform_review_id=review.platform_review_id,
            business_id=review.business_id,
            author_name=review.author_name,
            rating=review.rating,
            text=review.text,
            review_date=review.review_date,
            sentiment=sentiment_result.get('label'),
            sentiment_score=sentiment_result.get('score'),
            emotions=json.dumps(emotion_result),
            aspects=json.dumps(aspect_result),
            ai_response=ai_response,
            created_at=datetime.utcnow()
        )
        
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
    """Create multiple reviews with mock NLP"""
    try:
        created_count = 0
        skipped_count = 0
        
        for review_data in bulk.reviews:
            existing = db.query(Review).filter(
                Review.platform_review_id == review_data.get('platform_review_id', '')
            ).first()
            
            if existing:
                skipped_count += 1
                continue
            
            rating = review_data.get('rating', 0)
            text = review_data.get('text', '')
            
            sentiment_result = mock_sentiment_analysis(text, rating)
            emotion_result = mock_emotion_detection(text, rating)
            aspect_result = mock_aspect_extraction(text)
            ai_response = mock_response_generator(text, sentiment_result['label'])
            
            new_review = Review(
                platform=review_data.get('platform', 'manual'),
                platform_review_id=review_data.get('platform_review_id', f"manual_{datetime.now().timestamp()}"),
                business_id=bulk.business_id,
                author_name=review_data.get('author_name', 'Anonymous'),
                rating=rating,
                text=text,
                review_date=datetime.fromisoformat(review_data.get('review_date')) if review_data.get('review_date') else datetime.utcnow(),
                sentiment=sentiment_result.get('label'),
                sentiment_score=sentiment_result.get('score'),
                emotions=json.dumps(emotion_result),
                aspects=json.dumps(aspect_result),
                ai_response=ai_response,
                created_at=datetime.utcnow()
            )
            
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
    """Get all reviews for a restaurant"""
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

# ==================== GOOGLE PLACES INTEGRATION ====================

class GooglePlacesRequest(BaseModel):
    restaurant_name: str
    location: Optional[str] = ""
    business_id: int

@app.post("/api/google/fetch-reviews")
async def fetch_google_reviews_endpoint(request: GooglePlacesRequest, db: Session = Depends(get_db)):
    """
    Fetch real reviews from Google Places API
    
    Requires GOOGLE_PLACES_API_KEY in .env file
    """
    try:
        # Fetch reviews from Google
        google_reviews = fetch_google_reviews(request.restaurant_name, request.location)
        
        if not google_reviews:
            return {
                "success": False,
                "message": "No reviews found or API key not configured",
                "created": 0
            }
        
        # Store reviews with mock NLP
        created_count = 0
        skipped_count = 0
        
        for review_data in google_reviews:
            # Check if exists
            existing = db.query(Review).filter(
                Review.platform_review_id == review_data.get('platform_review_id', '')
            ).first()
            
            if existing:
                skipped_count += 1
                continue
            
            rating = review_data.get('rating', 0)
            text = review_data.get('text', '')
            
            # Mock NLP analysis
            sentiment_result = mock_sentiment_analysis(text, rating)
            emotion_result = mock_emotion_detection(text, rating)
            aspect_result = mock_aspect_extraction(text)
            ai_response = mock_response_generator(text, sentiment_result['label'])
            
            new_review = Review(
                platform=review_data.get('platform', 'google'),
                platform_review_id=review_data.get('platform_review_id'),
                business_id=request.business_id,
                author_name=review_data.get('author_name', 'Anonymous'),
                rating=rating,
                text=text,
                review_date=datetime.fromisoformat(review_data.get('review_date')) if review_data.get('review_date') else datetime.utcnow(),
                sentiment=sentiment_result.get('label'),
                sentiment_score=sentiment_result.get('score'),
                emotions=json.dumps(emotion_result),
                aspects=json.dumps(aspect_result),
                ai_response=ai_response,
                created_at=datetime.utcnow()
            )
            
            db.add(new_review)
            created_count += 1
        
        db.commit()
        
        return {
            "success": True,
            "created": created_count,
            "skipped": skipped_count,
            "total": len(google_reviews),
            "message": f"Fetched {created_count} reviews from Google Places"
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/google/restaurant-info")
async def get_google_restaurant_info(restaurant_name: str, location: str = ""):
    """Get restaurant information from Google Places"""
    try:
        info = get_restaurant_details(restaurant_name, location)
        if info:
            return {
                "success": True,
                "restaurant": info
            }
        else:
            return {
                "success": False,
                "message": "Restaurant not found or API key not configured"
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
    """Get analytics for a restaurant"""
    try:
        since_date = datetime.utcnow() - timedelta(days=days)
        
        # Only show approved reviews in analytics
        reviews = db.query(Review).filter(
            Review.business_id == restaurant_id,
            Review.review_date >= since_date,
            Review.approval_status == "approved"
        ).all()
        
        if not reviews:
            return {
                "success": True,
                "restaurant_id": restaurant_id,
                "period_days": days,
                "total_reviews": 0,
                "average_rating": 0.0,
                "sentiment_distribution": {"POSITIVE": 0, "NEUTRAL": 0, "NEGATIVE": 0},
                "top_emotions": {},
                "top_aspects": {},
                "rating_distribution": {
                    "5_star": 0,
                    "4_star": 0,
                    "3_star": 0,
                    "2_star": 0,
                    "1_star": 0
                },
                "message": "No reviews found in this time period"
            }
        
        sentiment_dist = {"POSITIVE": 0, "NEUTRAL": 0, "NEGATIVE": 0}
        emotion_dist = {}
        aspect_dist = {}
        ratings = []
        
        for review in reviews:
            if review.sentiment:
                sentiment_dist[review.sentiment] = sentiment_dist.get(review.sentiment, 0) + 1
            
            if review.emotions:
                try:
                    emotions = json.loads(review.emotions)
                    for emotion, score in emotions.items():
                        if emotion not in emotion_dist:
                            emotion_dist[emotion] = []
                        emotion_dist[emotion].append(score)
                except:
                    pass
            
            if review.aspects:
                try:
                    aspects = json.loads(review.aspects)
                    for aspect in aspects:
                        aspect_name = aspect.get('aspect', 'unknown')
                        aspect_dist[aspect_name] = aspect_dist.get(aspect_name, 0) + 1
                except:
                    pass
            
            if review.rating:
                ratings.append(review.rating)
        
        avg_rating = sum(ratings) / len(ratings) if ratings else 0
        
        top_emotions = {
            emotion: round(sum(scores) / len(scores), 3)
            for emotion, scores in emotion_dist.items()
        }
        top_emotions = dict(sorted(top_emotions.items(), key=lambda x: x[1], reverse=True)[:5])
        
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
    """Get sentiment distribution"""
    try:
        since_date = datetime.utcnow() - timedelta(days=days)
        
        # Only show approved reviews in analytics
        query = db.query(Review).filter(
            Review.review_date >= since_date,
            Review.approval_status == "approved"
        )
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
        
        # Only show approved reviews in analytics
        query = db.query(Review).filter(
            Review.review_date >= since_date,
            Review.approval_status == "approved"
        )
        if business_id:
            query = query.filter(Review.business_id == business_id)
        
        reviews = query.all()
        
        emotion_counts = {}
        for review in reviews:
            if review.emotions:
                try:
                    emotions = json.loads(review.emotions)
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
    """Get overall stats"""
    try:
        # Get all reviews (only approved for analytics)
        total_reviews = db.query(Review).filter(Review.approval_status == "approved").count()
        total_businesses = db.query(Business).count()
        
        # Count pending reviews (waiting for approval)
        pending_reviews = db.query(Review).filter(Review.approval_status == "pending").count()
        
        # Only count approved reviews with AI responses
        reviews_with_ai = db.query(Review).filter(
            Review.ai_response.isnot(None),
            Review.approval_status == "approved"
        ).count()
        
        # Calculate average rating (only approved reviews)
        avg_rating = db.query(func.avg(Review.rating)).filter(
            Review.approval_status == "approved"
        ).scalar() or 0
        
        return {
            "success": True,
            "total_reviews": total_reviews,
            "total_restaurants": total_businesses,
            "response_stats": {
                "total_reviews": total_reviews,
                "approved_responses": reviews_with_ai,
                "posted_responses": 0,
                "pending_reviews": pending_reviews,
                "approval_rate": (reviews_with_ai / total_reviews * 100) if total_reviews > 0 else 0,
                "post_rate": 0
            },
            "average_rating": round(avg_rating, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== REVIEW APPROVAL ENDPOINTS ====================

class ReviewApproval(BaseModel):
    is_genuine: bool
    approval_notes: Optional[str] = ""
    approved_by: str = "admin"

@app.get("/api/reviews/pending")
async def get_pending_reviews(db: Session = Depends(get_db)):
    """Get all reviews pending approval"""
    try:
        reviews = db.query(Review).filter(
            Review.approval_status == "pending"
        ).order_by(Review.created_at.desc()).all()
        
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
                    "primary_emotion": r.primary_emotion,
                    "created_at": r.created_at.isoformat() if r.created_at else None,
                    "approval_status": r.approval_status
                }
                for r in reviews
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/reviews/{review_id}/approve")
async def approve_review(
    review_id: int,
    approval: ReviewApproval,
    db: Session = Depends(get_db)
):
    """Approve or reject a review"""
    try:
        review = db.query(Review).filter(Review.id == review_id).first()
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        
        review.is_genuine = approval.is_genuine
        review.approval_status = "approved" if approval.is_genuine else "rejected"
        review.approved_by = approval.approved_by
        review.approval_notes = approval.approval_notes
        review.approved_at = datetime.utcnow()
        
        db.commit()
        
        return {
            "success": True,
            "message": f"Review {'approved' if approval.is_genuine else 'rejected'} successfully",
            "review_id": review_id,
            "status": review.approval_status
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/reviews/stats")
async def get_review_stats(db: Session = Depends(get_db)):
    """Get review approval statistics"""
    try:
        total = db.query(Review).count()
        pending = db.query(Review).filter(Review.approval_status == "pending").count()
        approved = db.query(Review).filter(Review.approval_status == "approved").count()
        rejected = db.query(Review).filter(Review.approval_status == "rejected").count()
        
        return {
            "success": True,
            "stats": {
                "total": total,
                "pending": pending,
                "approved": approved,
                "rejected": rejected
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== RESPONSE APPROVAL ENDPOINTS ====================

class ResponseApproval(BaseModel):
    approved: bool
    final_response: Optional[str] = None
    approved_by: str = "admin"

@app.get("/api/responses/pending")
async def get_pending_responses(db: Session = Depends(get_db)):
    """Get all reviews with AI responses pending human approval"""
    try:
        reviews = db.query(Review).filter(
            Review.ai_response.isnot(None),
            Review.human_approved == False
        ).order_by(Review.created_at.desc()).all()
        
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
                    "created_at": r.created_at.isoformat() if r.created_at else None
                }
                for r in reviews
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/responses/{review_id}/approve")
async def approve_response(
    review_id: int,
    approval: ResponseApproval,
    db: Session = Depends(get_db)
):
    """Approve or reject an AI-generated response"""
    try:
        review = db.query(Review).filter(Review.id == review_id).first()
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        
        if approval.approved:
            # If human edited the response, use that, otherwise use AI response
            review.final_response = approval.final_response if approval.final_response else review.ai_response
            review.human_approved = True
            message = "Response approved and ready to post"
        else:
            # Rejected - clear the response
            review.final_response = None
            review.human_approved = False
            message = "Response rejected"
        
        review.updated_at = datetime.utcnow()
        db.commit()
        
        return {
            "success": True,
            "message": message,
            "review_id": review_id,
            "approved": approval.approved
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/responses/stats")
async def get_response_stats(db: Session = Depends(get_db)):
    """Get response approval statistics"""
    try:
        total_with_ai = db.query(Review).filter(Review.ai_response.isnot(None)).count()
        pending = db.query(Review).filter(
            Review.ai_response.isnot(None),
            Review.human_approved == False
        ).count()
        approved = db.query(Review).filter(Review.human_approved == True).count()
        posted = db.query(Review).filter(Review.response_posted == True).count()
        
        return {
            "success": True,
            "stats": {
                "total_with_ai_response": total_with_ai,
                "pending_approval": pending,
                "approved": approved,
                "posted": posted
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting RevuIQ Simple API (No ML Models)...")
    print("📊 Initializing database...")
    init_db()
    print("✓ Database ready!")
    print("\n⚠️  NOTE: Using mock NLP analysis (no ML models)")
    print("🔥 Server starting on http://localhost:8000")
    
    uvicorn.run(
        "simple_api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
