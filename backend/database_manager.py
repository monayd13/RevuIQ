"""
Database Manager for RevuIQ
Handles database connections, CRUD operations, and queries
"""

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, Session
from models import Base, Business, Review, Analytics, User, APIKey
from typing import List, Optional, Dict
from datetime import datetime, timedelta
import json

class DatabaseManager:
    """Manages all database operations"""
    
    def __init__(self, database_url: str = "sqlite:///./revuiq.db"):
        """
        Initialize database connection
        
        Args:
            database_url: SQLAlchemy database URL
                         - SQLite: "sqlite:///./revuiq.db"
                         - PostgreSQL: "postgresql://user:pass@localhost/dbname"
        """
        self.engine = create_engine(database_url, echo=False)
        self.SessionLocal = sessionmaker(bind=self.engine)
        
        # Create all tables
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self) -> Session:
        """Get a new database session"""
        return self.SessionLocal()
    
    # ==================== BUSINESS OPERATIONS ====================
    
    def create_business(self, name: str, platform: str, platform_id: str, 
                       category: str = None, location: str = None) -> Business:
        """Create a new business"""
        session = self.get_session()
        try:
            business = Business(
                name=name,
                platform=platform,
                platform_id=platform_id,
                category=category,
                location=location
            )
            session.add(business)
            session.commit()
            session.refresh(business)
            return business
        finally:
            session.close()
    
    def get_business(self, business_id: int) -> Optional[Business]:
        """Get business by ID"""
        session = self.get_session()
        try:
            return session.query(Business).filter(Business.id == business_id).first()
        finally:
            session.close()
    
    def get_business_by_platform_id(self, platform_id: str) -> Optional[Business]:
        """Get business by platform ID"""
        session = self.get_session()
        try:
            return session.query(Business).filter(Business.platform_id == platform_id).first()
        finally:
            session.close()
    
    # ==================== REVIEW OPERATIONS ====================
    
    def create_review(self, business_id: int, platform: str, text: str,
                     author: str = None, rating: float = None,
                     platform_review_id: str = None,
                     review_date: datetime = None) -> Review:
        """Create a new review"""
        session = self.get_session()
        try:
            review = Review(
                business_id=business_id,
                platform=platform,
                platform_review_id=platform_review_id,
                author=author,
                rating=rating,
                text=text,
                review_date=review_date or datetime.utcnow()
            )
            session.add(review)
            session.commit()
            session.refresh(review)
            return review
        finally:
            session.close()
    
    def update_review_analysis(self, review_id: int, sentiment: str, 
                              sentiment_score: float, polarity: float,
                              subjectivity: float, primary_emotion: str,
                              emotion_confidence: float, aspects: List[str] = None,
                              ai_response: str = None, response_tone: str = None,
                              response_confidence: float = None):
        """Update review with NLP analysis results"""
        session = self.get_session()
        try:
            review = session.query(Review).filter(Review.id == review_id).first()
            if review:
                review.sentiment = sentiment
                review.sentiment_score = sentiment_score
                review.polarity = polarity
                review.subjectivity = subjectivity
                review.primary_emotion = primary_emotion
                review.emotion_confidence = emotion_confidence
                review.aspects = json.dumps(aspects) if aspects else None
                review.ai_response = ai_response
                review.response_tone = response_tone
                review.response_confidence = response_confidence
                review.processed = True
                session.commit()
        finally:
            session.close()
    
    def approve_response(self, review_id: int, final_response: str = None):
        """Approve AI response (optionally with edits)"""
        session = self.get_session()
        try:
            review = session.query(Review).filter(Review.id == review_id).first()
            if review:
                review.human_approved = True
                review.final_response = final_response or review.ai_response
                session.commit()
        finally:
            session.close()
    
    def post_response(self, review_id: int):
        """Mark response as posted"""
        session = self.get_session()
        try:
            review = session.query(Review).filter(Review.id == review_id).first()
            if review:
                review.response_posted = True
                review.posted_at = datetime.utcnow()
                session.commit()
        finally:
            session.close()
    
    def get_review(self, review_id: int) -> Optional[Review]:
        """Get review by ID"""
        session = self.get_session()
        try:
            return session.query(Review).filter(Review.id == review_id).first()
        finally:
            session.close()
    
    def get_reviews_by_business(self, business_id: int, limit: int = 100) -> List[Review]:
        """Get all reviews for a business"""
        session = self.get_session()
        try:
            return session.query(Review).filter(
                Review.business_id == business_id
            ).order_by(Review.created_at.desc()).limit(limit).all()
        finally:
            session.close()
    
    def get_pending_reviews(self, limit: int = 50) -> List[Review]:
        """Get reviews pending human approval"""
        session = self.get_session()
        try:
            return session.query(Review).filter(
                Review.processed == True,
                Review.human_approved == False
            ).order_by(Review.created_at.desc()).limit(limit).all()
        finally:
            session.close()
    
    # ==================== ANALYTICS OPERATIONS ====================
    
    def get_sentiment_distribution(self, business_id: int = None, 
                                   days: int = 30) -> Dict:
        """Get sentiment distribution"""
        session = self.get_session()
        try:
            query = session.query(
                Review.sentiment,
                func.count(Review.id).label('count')
            )
            
            if business_id:
                query = query.filter(Review.business_id == business_id)
            
            # Last N days
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            query = query.filter(Review.created_at >= cutoff_date)
            
            results = query.group_by(Review.sentiment).all()
            
            return {
                sentiment: count for sentiment, count in results
            }
        finally:
            session.close()
    
    def get_emotion_distribution(self, business_id: int = None,
                                days: int = 30) -> Dict:
        """Get emotion distribution"""
        session = self.get_session()
        try:
            query = session.query(
                Review.primary_emotion,
                func.count(Review.id).label('count')
            )
            
            if business_id:
                query = query.filter(Review.business_id == business_id)
            
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            query = query.filter(Review.created_at >= cutoff_date)
            
            results = query.group_by(Review.primary_emotion).all()
            
            return {
                emotion: count for emotion, count in results if emotion
            }
        finally:
            session.close()
    
    def get_sentiment_trend(self, business_id: int = None, days: int = 30) -> List[Dict]:
        """Get sentiment trend over time"""
        session = self.get_session()
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            query = session.query(
                func.date(Review.created_at).label('date'),
                Review.sentiment,
                func.count(Review.id).label('count')
            ).filter(Review.created_at >= cutoff_date)
            
            if business_id:
                query = query.filter(Review.business_id == business_id)
            
            results = query.group_by(
                func.date(Review.created_at),
                Review.sentiment
            ).order_by(func.date(Review.created_at)).all()
            
            return [
                {
                    'date': str(date),
                    'sentiment': sentiment,
                    'count': count
                }
                for date, sentiment, count in results
            ]
        finally:
            session.close()
    
    def get_average_rating(self, business_id: int = None, days: int = 30) -> float:
        """Get average rating"""
        session = self.get_session()
        try:
            query = session.query(func.avg(Review.rating))
            
            if business_id:
                query = query.filter(Review.business_id == business_id)
            
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            query = query.filter(Review.created_at >= cutoff_date)
            
            result = query.scalar()
            return float(result) if result else 0.0
        finally:
            session.close()
    
    def get_response_stats(self, business_id: int = None) -> Dict:
        """Get response statistics"""
        session = self.get_session()
        try:
            query = session.query(Review)
            
            if business_id:
                query = query.filter(Review.business_id == business_id)
            
            total = query.count()
            approved = query.filter(Review.human_approved == True).count()
            posted = query.filter(Review.response_posted == True).count()
            
            return {
                'total_reviews': total,
                'approved_responses': approved,
                'posted_responses': posted,
                'approval_rate': (approved / total * 100) if total > 0 else 0,
                'post_rate': (posted / total * 100) if total > 0 else 0
            }
        finally:
            session.close()
    
    # ==================== USER OPERATIONS ====================
    
    def create_user(self, email: str, username: str, hashed_password: str,
                   full_name: str = None, role: str = "moderator") -> User:
        """Create a new user"""
        session = self.get_session()
        try:
            user = User(
                email=email,
                username=username,
                hashed_password=hashed_password,
                full_name=full_name,
                role=role
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        finally:
            session.close()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        session = self.get_session()
        try:
            return session.query(User).filter(User.email == email).first()
        finally:
            session.close()

# Initialize global database manager
db_manager = DatabaseManager()
