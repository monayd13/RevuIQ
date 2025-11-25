"""
Database configuration and models
Using SQLAlchemy with PostgreSQL (Supabase)
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL - Use SQLite by default
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./revuiq.db"
)

# Create engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ==================== MODELS ====================

class Business(Base):
    """Business/Restaurant model"""
    __tablename__ = "businesses"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    industry = Column(String)  # restaurant, hotel, retail, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    reviews = relationship("Review", back_populates="business")
    users = relationship("User", back_populates="business")


class User(Base):
    """User model (business owners/managers)"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(String, default="manager")  # admin, manager, viewer
    business_id = Column(Integer, ForeignKey("businesses.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    business = relationship("Business", back_populates="users")


class Review(Base):
    """Review model"""
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String, nullable=False)  # google, yelp, tripadvisor, meta
    platform_review_id = Column(String, unique=True, nullable=False)
    business_id = Column(Integer, ForeignKey("businesses.id"))
    
    # Review content
    author_name = Column(String)
    rating = Column(Float, nullable=False)
    text = Column(Text, nullable=False)
    review_date = Column(DateTime, nullable=False)
    
    # NLP Analysis
    sentiment = Column(String)  # POSITIVE, NEUTRAL, NEGATIVE
    sentiment_score = Column(Float)
    emotions = Column(Text)  # JSON string of emotions
    aspects = Column(Text)  # JSON string of aspects
    
    # Response
    ai_response = Column(Text)
    response_tone = Column(String)
    response_confidence = Column(Float)
    human_approved = Column(Boolean, default=False)
    final_response = Column(Text)
    response_posted = Column(Boolean, default=False)
    posted_at = Column(DateTime)
    
    # Review approval/verification
    is_genuine = Column(Boolean, default=None, nullable=True)
    approval_status = Column(String, default="pending")  # pending, approved, rejected
    approved_by = Column(String)
    approval_notes = Column(Text)
    approved_at = Column(DateTime)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    processed = Column(Boolean, default=False)
    primary_emotion = Column(String)
    
    # Relationships
    business = relationship("Business", back_populates="reviews")


class APIIntegration(Base):
    """API integration credentials"""
    __tablename__ = "api_integrations"
    
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"))
    platform = Column(String, nullable=False)  # google, yelp, meta
    api_key = Column(String)
    api_secret = Column(String)
    access_token = Column(String)
    refresh_token = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Analytics(Base):
    """Analytics and metrics"""
    __tablename__ = "analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"))
    date = Column(DateTime, nullable=False)
    
    # Metrics
    total_reviews = Column(Integer, default=0)
    positive_reviews = Column(Integer, default=0)
    neutral_reviews = Column(Integer, default=0)
    negative_reviews = Column(Integer, default=0)
    average_rating = Column(Float, default=0.0)
    response_rate = Column(Float, default=0.0)
    avg_response_time = Column(Float, default=0.0)  # in hours
    
    created_at = Column(DateTime, default=datetime.utcnow)


# ==================== DATABASE FUNCTIONS ====================

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created!")


def drop_db():
    """Drop all database tables (use with caution!)"""
    Base.metadata.drop_all(bind=engine)
    print("✓ Database tables dropped!")


# ==================== CRUD OPERATIONS ====================

class ReviewCRUD:
    """CRUD operations for reviews"""
    
    @staticmethod
    def create_review(db, review_data):
        """Create a new review"""
        review = Review(**review_data)
        db.add(review)
        db.commit()
        db.refresh(review)
        return review
    
    @staticmethod
    def get_review(db, review_id):
        """Get review by ID"""
        return db.query(Review).filter(Review.id == review_id).first()
    
    @staticmethod
    def get_reviews_by_business(db, business_id, skip=0, limit=100):
        """Get all reviews for a business"""
        return db.query(Review).filter(
            Review.business_id == business_id
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_review_analysis(db, review_id, sentiment, emotions, aspects=None):
        """Update review with NLP analysis"""
        review = db.query(Review).filter(Review.id == review_id).first()
        if review:
            review.sentiment = sentiment.get('label')
            review.sentiment_score = sentiment.get('score')
            review.emotions = str(emotions)  # Convert to JSON string
            if aspects:
                review.aspects = str(aspects)
            review.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(review)
        return review
    
    @staticmethod
    def add_ai_response(db, review_id, ai_response):
        """Add AI-generated response to review"""
        review = db.query(Review).filter(Review.id == review_id).first()
        if review:
            review.ai_response = ai_response
            review.response_status = "pending_approval"
            review.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(review)
        return review


if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Database ready!")
