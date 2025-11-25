"""
Database Models for RevuIQ
SQLAlchemy ORM models for reviews, responses, and analytics
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Business(Base):
    """Business/Restaurant entity"""
    __tablename__ = "businesses"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    platform = Column(String(50))  # google, yelp, tripadvisor, meta
    platform_id = Column(String(255), unique=True)
    category = Column(String(100))
    location = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    reviews = relationship("Review", back_populates="business")

class Review(Base):
    """Customer review entity"""
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"))
    
    # Review details
    platform = Column(String(50), nullable=False)  # google, yelp, etc.
    platform_review_id = Column(String(255), unique=True)
    author_name = Column(String(255))
    rating = Column(Float)
    text = Column(Text, nullable=False)
    review_date = Column(DateTime)
    
    # NLP Analysis results
    sentiment = Column(String(20))  # POSITIVE, NEGATIVE, NEUTRAL
    sentiment_score = Column(Float)
    polarity = Column(Float)
    subjectivity = Column(Float)
    primary_emotion = Column(String(50))
    emotion_confidence = Column(Float)
    emotions = Column(Text)  # JSON string of all emotions
    aspects = Column(Text)  # JSON string of extracted aspects
    
    # Response management
    ai_response = Column(Text)
    response_tone = Column(String(50))
    response_confidence = Column(Float)
    human_approved = Column(Boolean, default=False)
    final_response = Column(Text)  # After human editing
    response_posted = Column(Boolean, default=False)
    posted_at = Column(DateTime)
    
    # Review approval/verification
    is_genuine = Column(Boolean, default=None, nullable=True)  # None=pending, True=genuine, False=fake
    approval_status = Column(String(20), default="pending")  # pending, approved, rejected
    approved_by = Column(String(255))  # Username who approved/rejected
    approval_notes = Column(Text)  # Notes about why approved/rejected
    approved_at = Column(DateTime)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    processed = Column(Boolean, default=False)
    
    # Relationships
    business = relationship("Business", back_populates="reviews")
    analytics = relationship("Analytics", back_populates="review", uselist=False)

class Analytics(Base):
    """Analytics and metrics for reviews"""
    __tablename__ = "analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    review_id = Column(Integer, ForeignKey("reviews.id"), unique=True)
    
    # Sentiment distribution
    positive_count = Column(Integer, default=0)
    negative_count = Column(Integer, default=0)
    neutral_count = Column(Integer, default=0)
    
    # Emotion distribution
    joy_count = Column(Integer, default=0)
    anger_count = Column(Integer, default=0)
    disappointment_count = Column(Integer, default=0)
    gratitude_count = Column(Integer, default=0)
    frustration_count = Column(Integer, default=0)
    
    # Response metrics
    response_time_seconds = Column(Float)
    approval_time_seconds = Column(Float)
    edit_count = Column(Integer, default=0)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    review = relationship("Review", back_populates="analytics")

class User(Base):
    """User accounts for human-in-the-loop"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    role = Column(String(50), default="moderator")  # admin, moderator, viewer
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)

class APIKey(Base):
    """Platform API keys storage"""
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String(50), nullable=False)  # google, yelp, meta
    key_name = Column(String(100))
    api_key = Column(String(500), nullable=False)
    api_secret = Column(String(500))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
